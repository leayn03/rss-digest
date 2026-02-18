---
name: rss-digest
version: 1.4
description: Automated RSS feed aggregation and daily digest generation with AI-powered curation. Parses OPML subscription files, fetches articles from multiple RSS sources, generates comprehensive daily reports in Markdown and HTML formats. Features smart insight generation with optimized formatting for readability. Supports flexible Feishu (Lark) integration with two modes - append to existing documents or create new documents. Includes comprehensive testing and configuration tools. Use when the user wants to aggregate RSS feeds, create daily news digests, curate article collections, or automate information monitoring and team collaboration from multiple sources.
---

# RSS Digest v1.4

Automatically aggregate RSS feeds and generate AI-curated daily digest reports with seamless Feishu integration.

## 🎉 What's New in v1.4

### Feishu Integration Enhancements
- **✨ Dual Upload Modes**: Choose between append or create mode
  - **Append Mode**: Add daily reports to a single master document
  - **Create Mode**: Generate separate documents for each report
- **🛠️ Comprehensive Tooling**: Built-in testing and configuration utilities
  - `check_feishu_config.sh` - View current configuration
  - `test_feishu_connection.py` - Test API connectivity
  - `test_folder_permission.sh` - Verify folder permissions
- **📚 Enhanced Documentation**:
  - Complete setup guides for both modes
  - Troubleshooting workflows
  - Permission configuration guides
- **🔧 Improved Error Handling**: Clear diagnostics for permission issues
- **📂 Flexible Storage**: Support for root directory or specified folders
- **🔐 Smart Permission Detection**: Automatic detection and guidance for missing permissions

### Project Organization
- Reorganized project structure with dedicated directories
- Archived temporary files for cleaner repository
- Centralized documentation in `docs/` folder
- Unified script management in `scripts/`

## What's New in v1.3

- **Feishu Integration**: Automatically upload markdown reports to Feishu (Lark) documents
- **Team Collaboration**: Share reports directly to your team's Feishu workspace
- **Flexible Configuration**: Support both environment variables and command-line arguments
- **Optional Upload**: Feishu upload is optional - works without credentials

## What's New in v1.2

- **Fixed date filtering**: `--date` parameter now correctly filters articles by exact target date
- **Fixed report title date**: Report titles now correctly display the target article date
- **Always show all articles overview**: Complete article overview section in all reports

## What's New in v1.1

- **Optimized insight formatting**: Better readability with improved label formatting
- **Smart content selection**: Adaptive article selection based on volume and time window
- **Improved insight quality**: Context-specific insights with deep analysis
- **Complete workflow scripts**: Automated processing pipeline

## 📋 Overview

This skill enables you to:
1. Parse OPML files containing RSS feed subscriptions
2. Fetch articles from multiple RSS sources in parallel
3. Generate AI-powered summaries (200 words) and insights (1000 words)
4. Generate comprehensive daily reports (Markdown + HTML)
5. Smart selection based on article volume and time window
6. **Automatic or manual upload to Feishu with flexible modes**
7. **Complete testing and diagnostic tooling**

## 🚀 Quick Start

### Basic Usage

```bash
# Generate yesterday's digest
./generate_digest.sh

# Generate specific date
./generate_digest.sh -d 2026-02-15

# Use wider time window (48 hours)
./generate_digest.sh -w 48
```

The script automatically:
1. Parses OPML feeds
2. Fetches articles with date filtering
3. Generates AI summaries
4. Creates markdown & HTML reports
5. Uploads to Feishu (if configured)
6. Opens HTML report in browser

## 🔧 Feishu Integration Setup

### Step 1: Create Feishu App

1. Visit [Feishu Open Platform](https://open.feishu.cn/app/)
2. Create "企业自建应用" (Enterprise Self-Built App)
3. Record your **App ID** and **App Secret**

### Step 2: Configure Permissions

Enable these permissions in your app:
- ✅ `docx:document` - Document creation and editing
- ✅ `drive:drive` - Drive/folder access
- ✅ `drive:drive:readonly` - Drive read access (optional)

**Important**: Wait for admin approval if required

### Step 3: Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit configuration
vim .env
```

### Step 4: Choose Your Mode

#### Option A: Append Mode (Recommended for Daily Use)

All reports go into a single document:

```bash
# .env configuration
FEISHU_MODE=append
FEISHU_DOCUMENT_ID=your_document_id  # Get from document URL
```

**Benefits**:
- ✅ Single document for all reports
- ✅ Easy to share one link
- ✅ Complete historical archive
- ✅ Simple to manage

**Get Document ID**:
1. Create a new document in Feishu
2. Open the document
3. Get ID from URL: `https://xxx.feishu.cn/docx/{DOCUMENT_ID}`
4. Give the app edit access to this document

#### Option B: Create Mode (for Separate Archives)

Each report creates a new document:

```bash
# .env configuration
FEISHU_MODE=create
FEISHU_FOLDER_TOKEN=your_folder_token  # Optional
```

**Benefits**:
- ✅ Independent documents per day
- ✅ Flexible organization
- ✅ Easy to delete individual reports
- ✅ Can be moved to different folders

**Root Directory** (Easiest):
- Leave `FEISHU_FOLDER_TOKEN` commented out
- Documents created in root
- Manually move to folders as needed

**Specific Folder** (Requires Setup):
1. Create folder in Feishu Drive
2. Get token from URL: `https://xxx.feishu.cn/drive/folder/{FOLDER_TOKEN}`
3. **Note**: Folder permissions are complex - see troubleshooting below

### Step 5: Test Configuration

```bash
# Check configuration
./scripts/check_feishu_config.sh

# Test API connection
python3 scripts/test_feishu_connection.py

# Test folder permissions (create mode only)
./scripts/test_folder_permission.sh
```

## 📁 Project Structure

```
rss-digest/
├── generate_digest.sh           # Main automation script
├── .env                         # Configuration (git-ignored)
├── .env.example                 # Configuration template
│
├── rss-digest/
│   ├── scripts/                 # Python processing scripts
│   │   ├── parse_opml.py
│   │   ├── fetch_rss.py
│   │   ├── generate_summaries.py
│   │   ├── generate_insights.py
│   │   └── generate_report.py
│   └── opml/                    # RSS subscription files
│
├── scripts/                     # Utility scripts
│   ├── upload_to_feishu_v2.py  # Upload tool (v2, recommended)
│   ├── check_feishu_config.sh  # Configuration viewer
│   ├── test_feishu_connection.py  # Connection tester
│   └── test_folder_permission.sh  # Permission tester
│
├── docs/                        # Documentation
│   ├── FEISHU_INTEGRATION.md   # Complete setup guide
│   ├── FEISHU_MODES.md         # Mode comparison
│   └── FEISHU_QUICKSTART.md    # Quick start guide
│
├── output/                      # Generated reports
│   ├── digest_*.md
│   ├── digest_*.html
│   └── digest_*_feishu_url.txt
│
└── logs/                        # Execution logs
```

## 🔄 Detailed Workflow

### 1. Parse OPML File

Extract RSS feed URLs:

```bash
python rss-digest/scripts/parse_opml.py <opml_file> > data/feeds.json
```

### 2. Fetch Articles

Fetch from all feeds with date filtering:

```bash
# Last 24 hours
python rss-digest/scripts/fetch_rss.py data/feeds.json --window 24 > data/articles_raw.json

# Specific date
python rss-digest/scripts/fetch_rss.py data/feeds.json --date 2026-02-15 > data/articles_raw.json
```

Features:
- Parallel fetching (10 workers)
- Date-based filtering
- Graceful error handling
- Comprehensive logging

### 3. Generate AI Summaries

Generate 200-word summaries:

```bash
python rss-digest/scripts/generate_summaries.py
```

Creates `data/articles.json` with summaries. If not cached, prints prompt for AI.

### 4. Generate Deep Insights

Select articles and generate 1000-word insights:

```bash
python rss-digest/scripts/generate_insights.py
```

**Smart Selection**:
- Single day (≤24h) → All articles
- Multi-day + <10 articles → All articles
- Multi-day + ≥10 articles → Top 10

Creates `data/insights.json` or prints prompts.

### 5. Generate Reports

Create final reports:

```bash
python rss-digest/scripts/generate_report.py data/articles.json data/insights.json output/
```

Generates:
- `digest_YYYY-MM-DD.md` - Markdown
- `digest_YYYY-MM-DD.html` - Styled HTML

### 6. Upload to Feishu (Optional)

```bash
# Automatic (via environment config)
python3 scripts/upload_to_feishu_v2.py output/digest_2026-02-17.md

# Manual mode override
FEISHU_MODE=create python3 scripts/upload_to_feishu_v2.py output/digest_2026-02-17.md
```

## 🛠️ Configuration Management

### View Current Configuration

```bash
./scripts/check_feishu_config.sh
```

Shows:
- Current mode (append/create)
- Target document/folder
- Credential status
- Quick usage guide

### Switch Modes

Edit `.env` file:

```bash
# Switch to append mode
FEISHU_MODE=append
FEISHU_DOCUMENT_ID=BFf2dweffoJleixPUcscchUynNg

# Switch to create mode
FEISHU_MODE=create
# FEISHU_FOLDER_TOKEN=Pz1wfydIglHWBhdFmAicScuCn6e  # Optional
```

### Test Configuration

```bash
# Test basic connectivity
python3 scripts/test_feishu_connection.py

# Test folder permissions (create mode)
./scripts/test_folder_permission.sh

# Diagnose permission issues
python3 scripts/grant_folder_permission.py
```

## 🔍 Troubleshooting

### Issue: "no folder permission" Error

**Problem**: App cannot create documents in specified folder

**Solution A - Use Root Directory** (Recommended):
1. Comment out `FEISHU_FOLDER_TOKEN` in `.env`
2. Documents will be created in root
3. Manually move to desired folder in Feishu

**Solution B - Configure Drive Permissions**:
1. Visit [Feishu Open Platform](https://open.feishu.cn/app/)
2. Go to your app → Permissions
3. Enable: `drive:drive` or `drive:drive:readonly`
4. Click "Apply for Permission"
5. Wait for admin approval
6. Re-run `./scripts/test_folder_permission.sh`

**Note**: Adding apps to folder collaborators typically doesn't work due to Feishu's permission model. Root directory + manual move is the most reliable approach.

### Issue: Upload Fails with 403 Error

**Checks**:
1. Verify credentials: `./scripts/check_feishu_config.sh`
2. Test connection: `python3 scripts/test_feishu_connection.py`
3. Check permissions in Feishu app settings
4. Ensure permissions are approved (not pending)

### Issue: No Articles Found

**Solutions**:
```bash
# Widen time window
./generate_digest.sh -d 2026-02-15 -w 48

# Check logs
cat logs/fetch_YYYY-MM-DD.log

# Verify OPML feeds are accessible
python rss-digest/scripts/parse_opml.py rss-digest/opml/your-feeds.opml
```

### Issue: AI Generation Steps Hang

**Context**: Steps 3 and 4 require Claude AI interaction

**Workflow**:
1. Script prints prompt for AI
2. User sends prompt to Claude
3. User saves AI response to file
4. Script continues

**Tips**:
- Use Claude with large context window
- Save responses exactly as provided
- Check file paths match script expectations

## 📚 Documentation

- **[docs/FEISHU_INTEGRATION.md](../docs/FEISHU_INTEGRATION.md)** - Complete setup guide
- **[docs/FEISHU_MODES.md](../docs/FEISHU_MODES.md)** - Mode comparison and best practices
- **[docs/FEISHU_QUICKSTART.md](../docs/FEISHU_QUICKSTART.md)** - 5-minute setup
- **[PROJECT_STRUCTURE.md](../PROJECT_STRUCTURE.md)** - Project organization
- **[README.md](../README.md)** - Main project documentation
- **[CHANGELOG.md](../CHANGELOG.md)** - Version history

## 💡 Tips & Best Practices

### Content Selection
- **Single day reports**: Use default 24h window for focused daily content
- **Weekly roundups**: Use `-w 168` for 7-day window
- **Catch-up mode**: Use wider window after being offline

### Feishu Integration
- **Daily reports**: Use **append mode** to single document
- **Monthly archives**: Create new document each month, update `FEISHU_DOCUMENT_ID`
- **Team sharing**: Share master document once, all updates automatic
- **Storage**: Root directory is most reliable, manual organization as needed

### Formatting
- Avoid excessive bold labels in single-line contexts
- Use natural flowing text for insights
- Follow v1.1+ formatting guidelines for readability

### Performance
- Adjust parallel workers in `fetch_rss.py` based on network
- Monitor `logs/` for slow feeds
- Consider caching for frequently accessed feeds

### Security
- Never commit `.env` to version control
- Rotate App Secret periodically
- Use minimum required permissions
- Review logs for sensitive data before sharing

## 📦 Installation

```bash
# Install dependencies
pip install -r rss-digest/scripts/requirements.txt
```

Required packages:
- `feedparser` - RSS/Atom parsing
- `python-dateutil` - Date handling
- `requests` - HTTP client
- `python-dotenv` - Environment management

## 🎯 Example Workflows

### Daily Team Digest

```bash
# Setup (once)
cp .env.example .env
vim .env  # Configure append mode

# Daily use
./generate_digest.sh
```

### Weekly Research Roundup

```bash
# Generate last 7 days
./generate_digest.sh -w 168

# Review and curate in Feishu
# Share link with team
```

### Historical Analysis

```bash
# Generate reports for multiple days
for date in 2026-02-{10..17}; do
  ./generate_digest.sh -d $date
  sleep 5  # Rate limiting
done
```

### Manual Mode

```bash
# Step-by-step for custom workflow
python rss-digest/scripts/parse_opml.py feeds.opml > data/feeds.json
python rss-digest/scripts/fetch_rss.py data/feeds.json --date 2026-02-15 > data/articles_raw.json
python rss-digest/scripts/generate_summaries.py
python rss-digest/scripts/generate_insights.py
python rss-digest/scripts/generate_report.py data/articles.json data/insights.json output/
python3 scripts/upload_to_feishu_v2.py output/digest_2026-02-15.md
```

## 🔗 Related Resources

- [Feishu Open Platform](https://open.feishu.cn/)
- [Feishu API Documentation](https://open.feishu.cn/document/)
- [RSS 2.0 Specification](https://www.rssboard.org/rss-specification)
- [Atom Syndication Format](https://datatracker.ietf.org/doc/html/rfc4287)

## 📝 Version History

- **v1.4** (2026-02-18) - Enhanced Feishu integration with dual modes, comprehensive tooling
- **v1.3** (2026-02-18) - Initial Feishu integration
- **v1.2** (2026-02-17) - Date filtering fixes
- **v1.1** (2026-02-16) - Formatting and selection improvements
- **v1.0** (2026-02-15) - Initial release

---

**Last Updated**: 2026-02-18
**Maintained By**: RSS Digest Team
**License**: MIT
