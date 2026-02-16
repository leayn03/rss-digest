#!/usr/bin/env python3
"""
Smart article selection and insight generation prompt creator.
Selects articles for deep insights based on count and time window.
- Single day (≤24h window) → All articles get insights
- Multi-day + <10 articles → All articles get insights
- Multi-day + ≥10 articles → Top 10 articles get insights
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description='Select articles and generate insight prompts')
    parser.add_argument('--window', type=int, default=24, help='Time window in hours')
    parser.add_argument('--date', type=str, help='Target date (YYYY-MM-DD)')
    return parser.parse_args()


def select_articles(articles, window_hours, target_date=None):
    """
    Smart selection of articles for deep insights.

    Args:
        articles: List of article dictionaries
        window_hours: Time window in hours
        target_date: Target date string (YYYY-MM-DD) or None

    Returns:
        Tuple of (selected_articles, selection_info)
    """
    total = len(articles)

    # Determine selection mode
    if window_hours <= 24:
        # Single day mode: all articles
        mode = "all"
        selected = articles
        reason = f"Single day mode (≤24h window): all {total} articles get insights"
    elif total < 10:
        # Multi-day but few articles: all articles
        mode = "all"
        selected = articles
        reason = f"Multi-day mode with <10 articles: all {total} articles get insights"
    else:
        # Multi-day with many articles: top 10
        mode = "top10"
        selected = articles[:10]
        reason = f"Multi-day mode with ≥10 articles: top 10 articles get insights"

    selection_info = {
        "total_articles": total,
        "selected_count": len(selected),
        "mode": mode,
        "window_hours": window_hours,
        "target_date": target_date,
        "reason": reason,
        "selected_indices": list(range(len(selected))),
        "generated_at": datetime.now().isoformat()
    }

    return selected, selection_info


def generate_insights_prompt(selected_articles, selection_info):
    """Generate prompt for deep insights with optimized formatting (v1.1)."""
    mode_desc = "all" if selection_info['mode'] == 'all' else f"top {selection_info['selected_count']}"

    prompt = f"""请为以下{mode_desc}篇文章分别生成约1000字的深度分析。

## 分析要求

每篇深度分析应包含：

1. **核心观点解读** - 深入分析文章的主要论点和价值
2. **技术/概念剖析** - 详细解释涉及的技术细节或关键概念
3. **趋势关联** - 与当前行业趋势和技术发展的关联
4. **实践启示** - 对读者的实际应用价值和建议
5. **延伸思考** - 引发的深层问题和未来展望

## 格式要求 (v1.1)

请使用自然流畅的叙述方式，避免在单行文本中使用"**标签**：内容"的格式。

**推荐格式**：
- 使用完整的段落叙述
- 将标签信息自然融入句子中
- 例如："Yagge警告的场景值得深思。例如当你以10倍生产力工作8小时，结果是..."
- 而非："- **场景A**：你以10倍生产力工作8小时"

**内容要求**：
- 每篇分析约1000字
- 深入有见地，避免泛泛而谈
- 结合具体文章内容，提供独特视角
- 使用专业但易懂的中文表达

## 文章列表

"""

    for i, article in enumerate(selected_articles):
        prompt += f"\n### {i}. {article['title']}\n\n"
        prompt += f"**链接**: {article['link']}\n\n"
        prompt += f"**来源**: {article['source']}\n\n"

        if article.get('summary'):
            prompt += f"**摘要**: {article['summary'][:400]}\n\n"

        if article.get('published'):
            prompt += f"**发布时间**: {article['published'][:10]}\n\n"

        prompt += "---\n\n"

    prompt += """
## 返回格式

请以JSON格式返回，键为文章索引，值为深度分析内容：

```json
{
  "0": "第一篇的1000字深度分析...",
  "1": "第二篇的1000字深度分析...",
  "2": "第三篇的1000字深度分析..."
}
```

请确保每篇分析都有足够的深度和独特性。
"""

    return prompt


def main():
    args = parse_args()

    # Default paths
    work_dir = Path.cwd()
    articles_file = work_dir / "data" / "articles.json"
    metadata_file = work_dir / "data" / "insights_metadata.json"
    insights_file = work_dir / "data" / "insights.json"

    # Read articles
    with open(articles_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    print(f"Loaded {len(articles)} articles", file=sys.stderr)

    # Select articles
    selected, selection_info = select_articles(articles, args.window, args.date)

    print(f"\n{selection_info['reason']}", file=sys.stderr)
    print(f"✓ Selected {len(selected)} articles for deep insights", file=sys.stderr)

    # Save metadata
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(selection_info, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved selection metadata to {metadata_file}", file=sys.stderr)

    # Check if insights.json exists
    if insights_file.exists():
        print(f"\n✓ Found existing insights at {insights_file}", file=sys.stderr)
        with open(insights_file, 'r', encoding='utf-8') as f:
            insights = json.load(f)
        print(f"  Contains {len(insights)} insights", file=sys.stderr)
    else:
        # Generate and print prompt
        print("\n" + "="*80, file=sys.stderr)
        print("DEEP INSIGHTS GENERATION PROMPT", file=sys.stderr)
        print("="*80, file=sys.stderr)
        print("\n⚠️  Copy the following prompt and use it with Claude AI:", file=sys.stderr)
        print("\n" + "-"*80 + "\n")
        print(generate_insights_prompt(selected, selection_info))
        print("\n" + "-"*80 + "\n", file=sys.stderr)
        print(f"\nAfter getting the AI response, save it as:", file=sys.stderr)
        print(f"  {insights_file}", file=sys.stderr)
        print("\nThen run the report generation script.", file=sys.stderr)


if __name__ == "__main__":
    main()
