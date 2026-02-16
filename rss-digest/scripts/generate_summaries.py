#!/usr/bin/env python3
"""
Generate AI summaries for all articles.
Reads articles_raw.json and outputs articles.json with summaries added.
"""

import json
import sys
from pathlib import Path


def main():
    # Default paths
    work_dir = Path.cwd()
    raw_file = work_dir / "data" / "articles_raw.json"
    output_file = work_dir / "data" / "articles.json"

    # Read raw articles
    with open(raw_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    print(f"Loaded {len(articles)} articles from {raw_file}", file=sys.stderr)

    # Add empty summaries for now (will be filled by AI)
    for article in articles:
        if 'summary' not in article or not article['summary']:
            article['summary'] = ""

    # Check if we need to generate summaries
    needs_summaries = any(not a.get('summary') or len(a.get('summary', '')) < 50 for a in articles)

    if needs_summaries:
        print("\n" + "="*80, file=sys.stderr)
        print("Articles need AI summaries!", file=sys.stderr)
        print("="*80, file=sys.stderr)
        print("\nPlease use the following prompt with Claude to generate summaries:", file=sys.stderr)
        print("\n" + "-"*80 + "\n", file=sys.stderr)

        # Generate prompt
        prompt = """请为以下文章生成200字左右的中文摘要。对于没有摘要或摘要很短的文章，基于标题和来源推断其可能的内容。

输出格式：JSON数组，每个元素包含 index 和 summary 字段。

文章列表：
"""
        for i, article in enumerate(articles):
            prompt += f"\n{i}. [{article['title']}]({article['link']})\n"
            prompt += f"   来源: {article['source']}\n"
            if article.get('summary') and len(article['summary']) > 50:
                prompt += f"   现有摘要: {article['summary'][:500]}...\n"

        prompt += """

要求：
1. 每个摘要约200字
2. 突出文章的核心观点和价值
3. 使用清晰、专业的中文
4. 即使原文是英文，也要用中文总结

返回JSON格式：
[
  {"index": 0, "summary": "200字摘要..."},
  {"index": 1, "summary": "200字摘要..."}
]
"""
        print(prompt, file=sys.stderr)
        print("\n" + "-"*80, file=sys.stderr)
        print("\nAfter getting the AI response, save it as data/summaries.json", file=sys.stderr)
        print("Then run this script again to merge summaries.", file=sys.stderr)

        # Check if summaries.json exists
        summaries_file = work_dir / "data" / "summaries.json"
        if summaries_file.exists():
            print(f"\nFound {summaries_file}, merging summaries...", file=sys.stderr)
            with open(summaries_file, 'r', encoding='utf-8') as f:
                summaries = json.load(f)

            for item in summaries:
                idx = item['index']
                if 0 <= idx < len(articles):
                    articles[idx]['summary'] = item['summary']

            print(f"✓ Merged {len(summaries)} summaries", file=sys.stderr)
        else:
            # Output articles with empty summaries
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(articles, f, indent=2, ensure_ascii=False)
            return
    else:
        print("✓ All articles have summaries", file=sys.stderr)

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

    print(f"✓ Wrote {len(articles)} articles to {output_file}", file=sys.stderr)


if __name__ == "__main__":
    main()
