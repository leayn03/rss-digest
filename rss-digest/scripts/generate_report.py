#!/usr/bin/env python3
"""
Generate daily digest report from articles.
"""

import json
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict


def load_template(template_path: str) -> str:
    """Load template file."""
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def generate_markdown_report(articles: List[Dict], top_articles: List[Dict],
                             insights: Dict[int, str], output_path: str, selection_mode="all",
                             date_str: str = None):
    """
    Generate Markdown report.

    Args:
        articles: All articles
        top_articles: Top curated articles
        insights: Dictionary mapping article index to insight text
        output_path: Output file path
        selection_mode: "all" for all articles, "top10" for top 10 only
        date_str: Target date string (YYYY-MM-DD), if None will be derived from articles
    """
    # Get date from first article if not provided
    if not date_str and articles and articles[0].get('published'):
        date_str = articles[0]['published'].split('T')[0]
    else:
        date_str = date_str or datetime.now().strftime('%Y-%m-%d')

    top_count = len(top_articles)
    total_count = len(articles)

    # Determine title based on mode
    if selection_mode == "all" or top_count == total_count:
        section_title = f"## 📌 深度阅读（全部 {top_count} 篇）"
    else:
        section_title = f"## 📌 精选深度阅读（Top {top_count}）"

    # Group articles by category
    by_category = {}
    for article in articles:
        cat = article.get('category', 'Uncategorized')
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(article)

    md = [
        f"# 每日资讯报告 - {date_str}",
        "",
        f"本报告汇总了 {total_count} 篇文章，涵盖科技新闻、行业资讯和学术论文。",
        "",
        section_title,
        "",
    ]

    # Top articles with insights
    for i, article in enumerate(top_articles, 1):
        md.append(f"### {i}. [{article['title']}]({article['link']})")
        md.append(f"**来源**: {article['source']} | **分类**: {article['category']} | **发布时间**: {article.get('published', 'Unknown')}")
        md.append("")
        md.append(f"**摘要**: {article['summary'][:200]}...")
        md.append("")

        # Add insight if available
        if str(i-1) in insights:
            md.append(f"**💡 启发与洞察**:")
            md.append(insights[str(i-1)])
            md.append("")

        md.append("---")
        md.append("")

    # All articles by category
    md.append("## 📰 全部资讯概要")
    md.append("")

    for category in sorted(by_category.keys()):
            cat_articles = by_category[category]
            md.append(f"### {category} ({len(cat_articles)} 篇)")
            md.append("")

            for article in cat_articles:
                pub_date = article.get('published', 'Unknown')
                if pub_date and pub_date != 'Unknown':
                    pub_date = pub_date.split('T')[0]
                else:
                    pub_date = 'Unknown'

                md.append(f"- **[{article['title']}]({article['link']})**")
                md.append(f"  - 来源: {article['source']} | 时间: {pub_date}")

                if article.get('summary'):
                    md.append(f"  - {article['summary'][:150]}...")

                md.append("")

            md.append("")

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))


def extract_tags_from_article(article: Dict) -> List[str]:
    """Extract tags from article for filtering."""
    tags = []
    if article.get('category'):
        tags.append(article['category'])
    if article.get('source'):
        # Extract domain from source
        source = article['source'].split('.')[0]
        tags.append(source)
    return tags


def format_insight_html(insight_text: str) -> str:
    """
    Format insight text for HTML display.

    Converts markdown-like formatting to HTML:
    - Headers (## or ###) to h4/h5
    - Bold text to <strong>
    - Paragraphs to <p>
    - Bullet points to <li>
    """
    if not insight_text:
        return ''

    lines = insight_text.strip().split('\n')
    html_parts = []
    current_paragraph = []
    in_list = False

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            if current_paragraph:
                html_parts.append('<p>' + ' '.join(current_paragraph) + '</p>')
                current_paragraph = []
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            continue

        # Headers - close list and paragraph first
        if line.startswith('### '):
            if current_paragraph:
                html_parts.append('<p>' + ' '.join(current_paragraph) + '</p>')
                current_paragraph = []
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            header_text = line[4:].strip().replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            html_parts.append(f'<h5>{header_text}</h5>')
            continue
        elif line.startswith('## '):
            if current_paragraph:
                html_parts.append('<p>' + ' '.join(current_paragraph) + '</p>')
                current_paragraph = []
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            header_text = line[3:].strip().replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            html_parts.append(f'<h4>{header_text}</h4>')
            continue

        # Bullet points - close paragraph first
        if line.startswith('- '):
            if current_paragraph:
                html_parts.append('<p>' + ' '.join(current_paragraph) + '</p>')
                current_paragraph = []
            if not in_list:
                html_parts.append('<ul class="insight-list">')
                in_list = True
            # Remove bold markers and escape HTML special characters from list items
            item_text = line[2:].replace('**', '').strip()
            item_text = item_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            html_parts.append(f'<li>{item_text}</li>')
            continue

        # End list if we hit regular text
        if in_list:
            html_parts.append('</ul>')
            in_list = False

        # Regular text - collect for paragraph
        # First escape HTML special characters
        escaped_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        # Then convert **bold** to <strong>bold</strong> using regex
        formatted_line = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', escaped_line)
        current_paragraph.append(formatted_line)

    # Close any open elements
    if current_paragraph:
        html_parts.append('<p>' + ' '.join(current_paragraph) + '</p>')
    if in_list:
        html_parts.append('</ul>')

    return '\n'.join(html_parts)


def generate_html_report(articles: List[Dict], top_articles: List[Dict],
                        insights: Dict[int, str], output_path: str, template_path: str, selection_mode="all",
                        date_str: str = None):
    """
    Generate HTML report using template.

    Args:
        articles: All articles
        top_articles: Top curated articles
        insights: Dictionary mapping article index to insight text
        output_path: Output file path
        template_path: HTML template path
        selection_mode: "all" for all articles, "top10" for top 10 only
        date_str: Target date string (YYYY-MM-DD), if None will be derived from articles
    """
    # Get date from first article if not provided
    if not date_str and articles and articles[0].get('published'):
        date_str = articles[0]['published'].split('T')[0]
    else:
        date_str = date_str or datetime.now().strftime('%Y-%m-%d')

    top_count = len(top_articles)
    total_count = len(articles)

    # Determine section title based on mode
    if selection_mode == "all" or top_count == total_count:
        section_title = f"深度阅读（全部 {top_count} 篇）"
    else:
        section_title = f"精选深度阅读（Top {top_count}）"

    # Collect all unique tags for filter
    all_tags = set()
    for article in articles:
        all_tags.update(extract_tags_from_article(article))

    filter_tags_html = ''.join([
        f'<div class="filter-tag" data-filter="{tag}">{tag}</div>'
        for tag in sorted(all_tags)
    ])

    # Generate top articles HTML
    top_html = []
    for i, article in enumerate(top_articles, 1):
        insight = insights.get(str(i-1), '')

        pub_date = article.get('published', 'Unknown')
        if pub_date != 'Unknown':
            pub_date = pub_date.split('T')[0]

        # Generate tags
        article_tags = extract_tags_from_article(article)
        tags_html = ''.join([
            f'<span class="tag source-tag" title="来源">{article["source"]}</span>',
            f'<span class="tag" title="分类">{article["category"]}</span>',
            f'<span class="tag date-tag" title="日期">{pub_date}</span>'
        ])

        summary_text = article.get('summary', '')[:300] if article.get('summary') else '暂无摘要'

        # Format insight with proper HTML
        insight_html = ''
        if insight:
            formatted_insight = format_insight_html(insight)
            word_count = len(insight.replace(' ', '').replace('\n', ''))
            insight_html = f'''
            <div class="insight">
                <div class="insight-header">
                    <strong>💡 深度洞察</strong>
                    <span class="word-count">({word_count}字)</span>
                </div>
                <div class="insight-content">{formatted_insight}</div>
            </div>'''

        top_html.append(f'''
        <div class="article featured" data-tags='{" ".join(article_tags)}'>
            <div class="article-number">{i}</div>
            <h3><a href="{article['link']}" target="_blank">{article['title']}</a></h3>
            <div class="tags">{tags_html}</div>
            <p class="summary">{summary_text}...</p>
            {insight_html}
        </div>
        ''')

    # Group articles by category
    by_category = {}
    for article in articles:
        cat = article.get('category', 'Uncategorized')
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(article)

    # Generate category sections
    category_html = []
    # Always show all articles overview (even if all have insights)
    for category in sorted(by_category.keys()):
            cat_articles = by_category[category]

            articles_list = []
            for article in cat_articles:
                pub_date = article.get('published', 'Unknown')
                if pub_date and pub_date != 'Unknown':
                    pub_date = pub_date.split('T')[0]
                else:
                    pub_date = 'Unknown'

                articles_list.append(f'''
                <div class="article-item">
                    <h4><a href="{article['link']}" target="_blank">{article['title']}</a></h4>
                    <div class="meta">
                        <span class="source">{article['source']}</span>
                        <span class="date">{pub_date}</span>
                    </div>
                    {f'<p class="summary">{article["summary"][:150]}...</p>' if article.get('summary') else ''}
                </div>
                ''')

            category_html.append(f'''
            <div class="category-section">
                <h3>{category} <span class="count">({len(cat_articles)} 篇)</span></h3>
                {''.join(articles_list)}
            </div>
            ''')

    # Load template and replace placeholders
    template = load_template(template_path)
    html = template.replace('{{DATE}}', date_str)
    html = html.replace('{{TOTAL_COUNT}}', str(total_count))
    html = html.replace('{{TOP_COUNT}}', str(top_count))
    html = html.replace('{{SECTION_TITLE}}', section_title)
    html = html.replace('{{FILTER_TAGS}}', filter_tags_html)
    html = html.replace('{{TOP_ARTICLES}}', ''.join(top_html))

    # Remove the "All Articles" section title if no content (before replacing placeholder)
    if selection_mode == "all" and not category_html:
        html = html.replace('<h2><span class="emoji">📰</span>全部资讯</h2>\n            {{ALL_ARTICLES}}', '')

    html = html.replace('{{ALL_ARTICLES}}', ''.join(category_html))

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)


if __name__ == "__main__":
    # Support both 3-arg (old) and 4-arg (new) formats
    if len(sys.argv) == 4:
        # Old format: articles_json, insights_json, output_dir
        articles_file = sys.argv[1]
        insights_file = sys.argv[2]
        output_dir = Path(sys.argv[3])
        top_articles_file = None
    elif len(sys.argv) == 5:
        # New format: articles_json, top_articles_json, insights_json, output_dir
        articles_file = sys.argv[1]
        top_articles_file = sys.argv[2]
        insights_file = sys.argv[3]
        output_dir = Path(sys.argv[4])
    else:
        print("Usage: python generate_report.py <articles_json> [top_articles_json] <insights_json> <output_dir>")
        print("\nFormats:")
        print("  Old (3 args): articles_json insights_json output_dir")
        print("  New (4 args): articles_json top_articles_json insights_json output_dir")
        sys.exit(1)

    # Load data
    with open(articles_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    with open(insights_file, 'r', encoding='utf-8') as f:
        insights = json.load(f)

    # Load or generate top_articles
    if top_articles_file:
        with open(top_articles_file, 'r', encoding='utf-8') as f:
            top_articles = json.load(f)
    else:
        # Use all articles with insights as top articles
        top_articles = []
        for idx_str in insights.keys():
            idx = int(idx_str)
            if idx < len(articles):
                top_articles.append(articles[idx])

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get template path - use v2 template
    script_dir = Path(__file__).parent.parent
    template_path = script_dir / 'assets' / 'report_template_v2.html'

    # Fallback to original template if v2 doesn't exist
    if not template_path.exists():
        template_path = script_dir / 'assets' / 'report_template.html'

    # Load selection metadata to determine mode
    selection_mode = "all"  # default
    metadata_file = Path(articles_file).parent / 'insights_metadata.json'
    if metadata_file.exists():
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
            selection_mode = metadata.get('mode', 'all')

    # Determine date from articles (use first article's date)
    date_str = datetime.now().strftime('%Y-%m-%d')  # fallback
    if articles and articles[0].get('published'):
        try:
            date_str = articles[0]['published'].split('T')[0]
        except:
            pass

    md_output = output_dir / f'digest_{date_str}.md'
    html_output = output_dir / f'digest_{date_str}.html'

    generate_markdown_report(articles, top_articles, insights, str(md_output), selection_mode, date_str)
    generate_html_report(articles, top_articles, insights, str(html_output), str(template_path), selection_mode, date_str)

    print(f"Reports generated:")
    print(f"  Markdown: {md_output}")
    print(f"  HTML: {html_output}")
