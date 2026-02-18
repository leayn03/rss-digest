#!/bin/bash

# RSS Daily Deep Insight Report Generator
# Updated to support date-based filtering and deep insights for ALL articles

set -e  # Exit on error

# Parse command line arguments
TARGET_DATE=""
WINDOW_HOURS=24

while getopts "d:w:h" opt; do
    case $opt in
        d) TARGET_DATE="$OPTARG" ;;
        w) WINDOW_HOURS="$OPTARG" ;;
        h)
            echo "Usage: $0 [-d DATE] [-w HOURS]"
            echo ""
            echo "Options:"
            echo "  -d DATE    Target date (YYYY-MM-DD), default: yesterday"
            echo "  -w HOURS   Time window in hours (default: 24)"
            echo ""
            echo "Examples:"
            echo "  $0                    # Yesterday's articles (default)"
            echo "  $0 -d 2026-02-15      # Specific date"
            echo "  $0 -w 48              # Wider time window"
            exit 0
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
    esac
done

# Set date for logging and output
if [ -z "$TARGET_DATE" ]; then
    DATE=$(date -v-1d +%Y-%m-%d 2>/dev/null || date -d yesterday +%Y-%m-%d 2>/dev/null)
    DATE_DESC="yesterday"
else
    DATE="$TARGET_DATE"
    DATE_DESC="$TARGET_DATE"
fi

WORK_DIR="$(cd "$(dirname "$0")" && pwd)"
OPML_FILE="$WORK_DIR/rss-digest/opml/hn-popular-blogs-2025.opml"
OUTPUT_DIR="$WORK_DIR/output"
DATA_DIR="$WORK_DIR/data"
LOG_DIR="$WORK_DIR/logs"

# Create directories
mkdir -p "$OUTPUT_DIR" "$DATA_DIR" "$LOG_DIR"

echo "=============================================="
echo "RSS Daily Deep Insight Report - $DATE"
echo "=============================================="
echo ""
echo "Target: $DATE_DESC (±${WINDOW_HOURS}h window)"
echo ""

cd "$WORK_DIR"

# Step 1: Parse OPML
echo "[Step 1/5] Parsing OPML file..."
python3 rss-digest/scripts/parse_opml.py "$OPML_FILE" 2>"$LOG_DIR/parse_$DATE.log" > "$DATA_DIR/feeds.json"
FEED_COUNT=$(python3 -c "import json; print(len(json.load(open('$DATA_DIR/feeds.json'))))")
echo "✓ Found $FEED_COUNT RSS feeds"
echo ""

# Step 2: Fetch articles for target date
echo "[Step 2/5] Fetching articles for $DATE_DESC..."
if [ -z "$TARGET_DATE" ]; then
    python3 rss-digest/scripts/fetch_rss.py "$DATA_DIR/feeds.json" --window "$WINDOW_HOURS" 2>"$LOG_DIR/fetch_$DATE.log" 1>"$DATA_DIR/articles_raw.json"
else
    python3 rss-digest/scripts/fetch_rss.py "$DATA_DIR/feeds.json" --date "$TARGET_DATE" --window "$WINDOW_HOURS" 2>"$LOG_DIR/fetch_$DATE.log" 1>"$DATA_DIR/articles_raw.json"
fi
ARTICLE_COUNT=$(python3 -c "import json; print(len(json.load(open('$DATA_DIR/articles_raw.json'))))")
echo "✓ Fetched $ARTICLE_COUNT articles for $DATE_DESC"
echo ""

if [ "$ARTICLE_COUNT" -eq 0 ]; then
    echo "❌ No articles found for $DATE_DESC."
    echo "Check $LOG_DIR/fetch_$DATE.log for details."
    echo ""
    echo "Suggestions:"
    echo "  - Try a wider time window: $0 -d $DATE -w 48"
    echo "  - Check if RSS feeds were updated on this date"
    exit 1
fi

# Step 3: Generate AI summaries
echo "[Step 3/5] Generating 200-word AI summaries..."
python3 rss-digest/scripts/generate_summaries.py 2>"$LOG_DIR/summaries_$DATE.log"
echo "✓ AI summaries generated for $ARTICLE_COUNT articles"
echo ""

# Step 4: Generate deep insights prompts (smart selection)
echo "[Step 4/5] Generating deep insights prompts..."
echo "⚠️  This step requires Claude AI to generate 1000-word insights."
echo ""
python3 rss-digest/scripts/select_top10_and_insights.py --window "$WINDOW_HOURS" 2>"$LOG_DIR/insights_$DATE.log"
echo ""

# Check if insights.json exists
if [ ! -f "$DATA_DIR/insights.json" ]; then
    echo "⚠️  insights.json not found."
    echo ""
    echo "Please:"
    echo "  1. Use the prompts above to generate insights with Claude"
    echo "  2. Save the JSON response to: $DATA_DIR/insights.json"
    echo "  3. Run this script again to generate the report"
    echo ""
    exit 0
fi

# Step 5: Generate reports
echo "[Step 5/5] Generating reports..."
python3 rss-digest/scripts/generate_report.py "$DATA_DIR/articles.json" "$DATA_DIR/insights.json" "$OUTPUT_DIR/" 2>"$LOG_DIR/report_$DATE.log"

if [ -f "$OUTPUT_DIR/digest_$DATE.html" ]; then
    echo ""
    echo "=============================================="
    echo "✅ RSS Daily Deep Insight Report Completed!"
    echo "=============================================="
    echo ""
    echo "📊 Statistics:"
    echo "  - Target Date: $DATE_DESC"
    echo "  - Articles: $ARTICLE_COUNT"
    echo "  - Deep Insights: $ARTICLE_COUNT (1000 words each)"
    echo ""
    echo "📄 Reports:"
    echo "  - Markdown: $OUTPUT_DIR/digest_$DATE.md"
    echo "  - HTML: $OUTPUT_DIR/digest_$DATE.html"
    echo ""
    echo "📝 Logs: $LOG_DIR/"
    echo ""

    # Upload to Feishu (optional)
    if [ -n "$FEISHU_APP_ID" ] && [ -n "$FEISHU_APP_SECRET" ]; then
        echo "📤 Uploading to Feishu document..."
        # Use v2 script which supports both append and create modes
        if python3 scripts/upload_to_feishu_v2.py "$OUTPUT_DIR/digest_$DATE.md" 2>"$LOG_DIR/feishu_$DATE.log"; then
            echo "✓ Successfully uploaded to Feishu!"
            if [ -f "$OUTPUT_DIR/digest_${DATE}_feishu_url.txt" ]; then
                echo "  URL: $(cat $OUTPUT_DIR/digest_${DATE}_feishu_url.txt)"
            fi
        else
            echo "⚠️  Feishu upload failed (check $LOG_DIR/feishu_$DATE.log)"
            echo "  This is optional - continuing..."
        fi
        echo ""
    fi

    # Open report
    echo "Opening HTML report..."
    open "$OUTPUT_DIR/digest_$DATE.html" 2>/dev/null || xdg-open "$OUTPUT_DIR/digest_$DATE.html" 2>/dev/null || echo "Please open: $OUTPUT_DIR/digest_$DATE.html"
else
    echo "❌ Report generation failed"
    echo "Check $LOG_DIR/report_$DATE.log for errors"
    exit 1
fi
