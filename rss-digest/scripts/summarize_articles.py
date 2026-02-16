#!/usr/bin/env python3
"""
Use AI to generate summaries for articles and select top articles.
"""

import json
import sys
from pathlib import Path


def generate_summaries_prompt(articles):
    """Generate prompt for article summarization."""
    prompt = """请为以下文章生成200字左右的中文摘要。对于没有摘要或摘要很短的文章，基于标题和来源推断其可能的内容。

输出格式：JSON数组，每个元素包含 index 和 summary 字段。

文章列表：
"""

    for i, article in enumerate(articles):
        prompt += f"\n{i}. [{article['title']}]({article['link']})\n"
        prompt += f"   来源: {article['source']}\n"
        if article.get('summary') and len(article['summary']) > 50:
            # 截取前500字符作为参考
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

    return prompt


def generate_top_selection_prompt(articles, top_n=10):
    """Generate prompt for selecting top articles."""
    prompt = f"""请从以下{len(articles)}篇文章中，根据以下标准选出最值得深度阅读的{top_n}篇文章：

评选标准：
1. 内容质量和深度
2. 时效性和相关性
3. 话题多样性（覆盖不同领域）
4. 实用价值和启发性
5. 来源的权威性

文章列表：
"""

    for i, article in enumerate(articles):
        prompt += f"\n{i}. [{article['title']}]({article['link']})\n"
        prompt += f"   来源: {article['source']} | 发布: {article.get('published', 'Unknown')[:10]}\n"
        if article.get('summary'):
            prompt += f"   摘要: {article['summary'][:200]}...\n"

    prompt += f"""

请返回JSON格式，包含选中文章的索引：
{{"selected_indices": [0, 3, 5, ...]}}

确保选出的{top_n}篇文章涵盖不同主题，避免重复话题。
"""

    return prompt


def generate_insights_prompt(articles):
    """Generate prompt for deep insights (1000 words each)."""
    prompt = """请为以下精选文章分别生成约1000字的深度分析。每篇分析应包含：

1. 文章核心观点的深入解读
2. 技术或概念的详细剖析
3. 与当前趋势和行业背景的关联
4. 对读者的实践启示和应用价值
5. 引发的深层思考和延伸问题

文章列表：
"""

    for i, article in enumerate(articles):
        prompt += f"\n{i}. [{article['title']}]({article['link']})\n"
        prompt += f"   来源: {article['source']}\n"
        if article.get('summary'):
            prompt += f"   摘要: {article['summary'][:300]}...\n"

    prompt += """

返回JSON格式：
{
  "0": "1000字深度分析...",
  "1": "1000字深度分析..."
}

每篇分析约1000字，要深入、有见地、有实践价值。
"""

    return prompt


def main():
    if len(sys.argv) != 2:
        print("Usage: python summarize_articles.py <articles_json>")
        print("\nThis script generates prompts for AI to:")
        print("1. Summarize all articles (~200 words each)")
        print("2. Select top 10 articles")
        print("3. Generate deep insights (1000 words each)")
        print("\nYou need to feed these prompts to an AI and save the responses.")
        sys.exit(1)

    articles_file = sys.argv[1]

    with open(articles_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    print(f"Loaded {len(articles)} articles")
    print("\n" + "="*80)
    print("STEP 1: Generate 200-word summaries for all articles")
    print("="*80)
    print(generate_summaries_prompt(articles))

    print("\n" + "="*80)
    print(f"STEP 2: Select top {10} articles")
    print("="*80)
    print(generate_top_selection_prompt(articles, 10))

    print("\n" + "="*80)
    print("STEP 3: Generate 1000-word insights for top articles")
    print("="*80)
    print("(Run this after you have the top 10 selection)")
    print("="*80)


if __name__ == "__main__":
    main()
