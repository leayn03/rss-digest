# RSS Digest 工作流程指南

## 📋 概述

完整的RSS资讯聚合和AI分析工作流程，支持：
- ✅ 从92个RSS源抓取最新文章
- ✅ AI生成200字摘要（每篇文章）
- ✅ AI筛选Top 10文章
- ✅ 生成1000字深度洞察（每篇精选文章）
- ✅ 精美的Markdown + HTML双格式报告
- ✅ 交互式标签筛选功能

## 🚀 快速开始

### 1. 安装依赖

```bash
cd rss-digest
pip install -r scripts/requirements.txt
```

### 2. 运行完整工作流程

```bash
./generate_digest.sh
```

这个脚本会引导你完成所有步骤，包括AI分析环节。

## 📝 详细工作流程

### 步骤 1: 解析OPML文件

```bash
python3 rss-digest/scripts/parse_opml.py rss-digest/opml/hn-popular-blogs-2025.opml > feeds.json
```

**输出**: `feeds.json` - 包含所有RSS源的列表

### 步骤 2: 抓取文章

```bash
python3 rss-digest/scripts/fetch_rss.py feeds.json > articles_raw.json 2>fetch.log
```

**输出**: `articles_raw.json` - 原始抓取的文章（可能没有摘要或摘要很短）

**注意**: 只抓取最近24小时内有明确发布日期的文章

### 步骤 3: AI摘要和筛选

这一步需要使用Claude AI进行三个任务：

#### 3.1 为所有文章生成200字摘要

```bash
python3 rss-digest/scripts/summarize_articles.py articles_raw.json
```

这会输出一个提示词。将提示词发送给Claude，然后：

1. Claude会返回包含所有文章摘要的JSON
2. 将摘要更新到`articles_raw.json`中
3. 保存为`articles.json`

**示例输出格式**:
```json
[
  {"index": 0, "summary": "200字摘要..."},
  {"index": 1, "summary": "200字摘要..."}
]
```

#### 3.2 筛选Top 10文章

使用Step 2的提示词（或者基于`articles.json`手动分析），选出Top 10文章。

**保存为**: `top_articles.json`

**示例格式**:
```json
[
  {
    "title": "Article Title",
    "link": "https://...",
    "summary": "200字摘要",
    "published": "2026-02-15T12:00:00",
    "source": "example.com",
    "category": "Tech",
    "author": "Author Name"
  }
]
```

#### 3.3 生成1000字深度洞察

为Top 10文章生成深度分析（每篇约1000字）。

**保存为**: `insights.json`

**示例格式**:
```json
{
  "0": "第一篇文章的1000字深度分析...",
  "1": "第二篇文章的1000字深度分析...",
  ...
  "9": "第十篇文章的1000字深度分析..."
}
```

### 步骤 4: 生成报告

```bash
python3 rss-digest/scripts/generate_report.py articles.json top_articles.json insights.json output/
```

**输出**:
- `output/digest_YYYY-MM-DD.md` - Markdown格式报告
- `output/digest_YYYY-MM-DD.html` - HTML格式报告（带标签筛选）

### 步骤 5: 查看报告

```bash
open output/digest_2026-02-15.html
```

## 🎨 HTML报告功能

新版HTML报告包含以下增强功能：

1. **标签筛选**: 点击顶部的筛选标签，快速过滤文章
2. **响应式设计**: 完美支持移动设备
3. **视觉层次**: Top 10文章突出显示，带有编号徽章
4. **交互式标签**: 点击文章的标签可以快速筛选相关内容
5. **深度洞察**: 1000字的深入分析，格式清晰易读

## 🤖 AI分析要点

### 文章摘要（200字）

要求：
- 突出核心观点和价值
- 清晰、专业的中文
- 即使原文英文也用中文总结

### Top 10筛选标准

- 内容质量和深度
- 时效性和相关性
- 话题多样性（覆盖不同领域）
- 实用价值和启发性
- 来源的权威性

### 深度洞察（1000字）

每篇分析应包含：
1. 文章核心观点的深入解读
2. 技术或概念的详细剖析
3. 与当前趋势和行业背景的关联
4. 对读者的实践启示和应用价值
5. 引发的深层思考和延伸问题

## 🔄 自动化

### 每日定时任务

创建cron job，每天8点自动运行：

```bash
0 8 * * * cd /path/to/rss-digest && ./generate_digest.sh
```

**注意**: AI分析步骤需要手动或通过API调用Claude完成

### Claude API集成

如果你有Claude API access，可以自动化AI分析：

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

# 调用Claude进行摘要生成
response = client.messages.create(
    model="claude-opus-4",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": summary_prompt}
    ]
)
```

## 📊 报告结构

### Markdown报告

```markdown
# 每日资讯报告 - YYYY-MM-DD

## 📌 精选深度阅读（Top 10）
[10篇精选文章 + 1000字洞察]

## 📰 全部资讯
[按分类组织的所有文章]
```

### HTML报告

- **Header**: 日期和统计信息
- **筛选栏**: 交互式标签筛选
- **Top 10**: 精选文章带深度分析
- **分类列表**: 所有文章按类别组织
- **Footer**: 生成信息和链接

## 🛠️ 故障排除

### 问题 1: SSL证书错误

**症状**: `certificate verify failed`

**解决**: 代码已包含SSL修复：
```python
import ssl
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context
```

### 问题 2: 没有抓取到文章

**可能原因**:
1. RSS源最近24小时内没有更新
2. 网络连接问题
3. RSS源格式问题

**解决**:
- 检查 `fetch.log` 查看详细错误
- 尝试增加时间窗口（修改`fetch_rss.py`中的`hours`参数）

### 问题 3: HTML报告样式显示不正常

**解决**: 确保使用 `report_template_v2.html` 模板

## 📁 文件说明

### 核心脚本

- `parse_opml.py`: OPML解析器
- `fetch_rss.py`: RSS抓取器（带SSL修复）
- `summarize_articles.py`: AI提示词生成器
- `generate_report.py`: 报告生成器

### 模板

- `report_template_v2.html`: 增强版HTML模板（带标签筛选）
- `report_template.html`: 原始HTML模板

### 数据文件

- `feeds.json`: RSS源列表
- `articles.json`: 所有文章（带摘要）
- `top_articles.json`: Top 10精选文章
- `insights.json`: 深度洞察

## 🎯 下一步优化

1. **Claude API集成**: 自动化AI分析步骤
2. **数据库存储**: 保存历史文章和分析
3. **趋势分析**: 跨时间的话题趋势分析
4. **推荐系统**: 基于用户兴趣的个性化推荐
5. **多语言支持**: 支持其他语言的文章和报告

## 📞 支持

如有问题，请查看：
- [SKILL.md](rss-digest/SKILL.md) - 技能详细说明
- [README.md](README.md) - 项目概述

---

**生成日期**: 2026-02-15
**版本**: 2.0
