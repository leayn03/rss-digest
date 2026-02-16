---
name: rss-digest
version: 1.2
description: Automated RSS feed aggregation and daily digest generation with AI-powered curation. Parses OPML subscription files, fetches articles from multiple RSS sources, generates comprehensive daily reports in Markdown and HTML formats. Features smart insight generation with optimized formatting for readability. Uses intelligent content selection (all articles for single-day feeds, top 10 for multi-day with 10+ articles) and AI-generated 1000-word deep insights. Use when the user wants to aggregate RSS feeds, create daily news digests, curate article collections, or automate information monitoring from multiple sources.
---

# RSS Digest v1.2

Automatically aggregate RSS feeds and generate AI-curated daily digest reports.

## What's New in v1.2

- **Fixed date filtering**: `--date` parameter now correctly filters articles by exact target date (previously ignored)
- **Fixed report title date**: Report titles now correctly display the target article date instead of current date
- **Always show all articles overview**: "全部资讯概要" section is now always displayed regardless of whether all articles have insights

## What's New in v1.1

- **Optimized insight formatting**: Removed excessive colons after bold labels in single-line contexts for better readability
- **Smart content selection**: Automatically adapts between "all articles" and "top 10" modes based on article count and time window
- **Improved insight quality**: Content-specific insights with contextual analysis instead of generic templates
- **Complete workflow scripts**: Added `generate_summaries.py` and `select_top10_and_insights.py` for automated processing

## Overview

This skill enables you to:
1. Parse OPML files containing RSS feed subscriptions
2. Fetch articles from multiple RSS sources in parallel
3. Generate AI-powered insights (1000 words) for selected articles
4. Generate comprehensive daily reports (Markdown + HTML)
5. Smart selection based on article volume and time window
6. Optimized formatting for comfortable reading experience

## Workflow

### 1. Parse OPML File

Use `parse_opml.py` to extract RSS feed URLs from an OPML subscription file:

```bash
python scripts/parse_opml.py <path_to_opml_file>
```

Save the output to a JSON file for the next step:

```bash
python scripts/parse_opml.py feeds.opml > data/feeds.json
```

### 2. Fetch Articles

Use `fetch_rss.py` to fetch articles from all feeds:

```bash
python scripts/fetch_rss.py data/feeds.json > data/articles_raw.json
```

Key features:
- Parallel fetching for performance (default 10 concurrent workers)
- Filters articles from last 24 hours (configurable with `--window` parameter)
- Extracts: title, link, summary, published date, source, category, author
- Handles malformed feeds gracefully

### 3. Generate Summaries

Use `generate_summaries.py` to generate AI summaries for all articles:

```bash
python scripts/generate_summaries.py
```

This creates `data/articles.json` with AI summaries added. If summaries are missing, it will print a prompt for Claude AI to generate summaries.

### 4. Smart Article Selection & Insight Generation

Use `select_top10_and_insights.py` to determine which articles need insights and generate prompts:

```bash
python scripts/select_top10_and_insights.py --window 24
```

**Smart Selection Rules**:
- Single day (≤24h window) → All articles get insights
- Multi-day + <10 articles → All articles get insights
- Multi-day + ≥10 articles → Top 10 articles get insights

This creates `data/insights_metadata.json` with selection info and prints Claude prompts for generating insights.

### 5. Generate Reports

Use `generate_report.py` to create final reports:

```bash
python scripts/generate_report.py data/articles.json data/insights.json output/
```

This generates:
- **Markdown report**: `output/digest_YYYY-MM-DD.md`
- **HTML report**: `output/digest_YYYY-MM-DD.html`

## Quick Start with Shell Script

Use the provided shell script for automation:

```bash
# Generate digest for yesterday (default)
./generate_digest.sh

# Generate digest for specific date
./generate_digest.sh -d 2026-02-15

# Use wider time window
./generate_digest.sh -w 48
```

## Insight Formatting Best Practices

The v1.1 update includes optimized formatting for insights to improve readability:

**Avoid** uncomfortable single-line patterns:
- ❌ `- **场景A**：你以10倍生产力工作8小时`
- ❌ `- **永远在线文化**：AI让随时随地工作成为可能`

**Use** natural flowing text:
- ✅ `例如当你以10倍生产力工作8小时，结果是雇主获得全部价值...`
- ✅ `AI让随时随地工作成为可能，催生了永远在线文化。`

This makes insights more readable and less visually cluttered.

## Installation

Install required dependencies:

```bash
pip install -r scripts/requirements.txt
```

Required packages:
- `feedparser`: RSS/Atom feed parsing

## Tips

- **Time window**: Use `--window` parameter to adjust the lookback period (default 24 hours)
- **Parallel fetching**: Adjust worker count in `fetch_rss.py` for performance tuning
- **Insight quality**: Use AI to generate content-specific insights rather than generic templates
- **Format consistency**: Follow the v1.1 formatting guidelines for better readability

## Example Usage

**Generate digest from OPML**:
```bash
# Parse feeds
python scripts/parse_opml.py feeds.opml > data/feeds.json

# Fetch articles (last 24 hours)
python scripts/fetch_rss.py data/feeds.json --window 24 > data/articles_raw.json

# Generate summaries (prompts for AI if needed)
python scripts/generate_summaries.py

# Select articles and generate insight prompts
python scripts/select_top10_and_insights.py --window 24

# After getting AI insights and saving to data/insights.json:
python scripts/generate_report.py data/articles.json data/insights.json output/
```

**Or use the automated script**:
```bash
./generate_digest.sh
```
