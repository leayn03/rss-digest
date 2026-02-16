# 更新日志 - Changelog

## v2.1.0 - 2026-02-16

### 🎯 智能深度分析策略

实现了根据时间窗口和文章数量自动选择最合适的分析策略，提供更灵活的报告生成方式。

### ✨ 新增功能

1. **智能分析策略选择**
   - 单日模式（≤24h窗口）：所有文章深度分析
   - 多日少量模式（>24h + <10篇）：所有文章深度分析
   - 多日精选模式（>24h + ≥10篇）：Top 10深度分析

2. **动态报告标题**
   - 根据分析策略自动调整报告标题和描述
   - 单日/少量：《RSS 每日深度分析报告》
   - 精选模式：《RSS 深度分析报告 - Top 10 精选》

3. **元数据管理**
   - 新增 `insights_metadata.json` 文件
   - 记录分析策略、文章数量、洞察数量等信息
   - 用于报告生成时的智能判断

### 🔄 改进的文件

#### 1. `select_top10_and_insights.py`
- 添加 `--window` 参数接收时间窗口
- 实现 `select_articles_for_insights()` 函数判断策略
- 生成包含策略信息的元数据文件
- 优化输出信息，清晰展示选择理由

#### 2. `generate_report.py`
- 添加 `load_metadata()` 函数读取元数据
- 添加 `get_report_title()` 函数生成动态标题
- 修改 Markdown 和 HTML 报告生成逻辑
- 支持 Top 10 和全文模式的不同布局

#### 3. `generate_digest.sh`
- 传递 `--window` 参数给 insights 生成脚本
- 保持现有的日期配置功能

#### 4. `report_template_v2.html`
- 支持动态标题占位符 `{{TITLE}}`
- 支持动态描述占位符 `{{DESCRIPTION}}`
- 简化内容区域，移除固定标题
- 自动适应不同的报告模式

#### 5. `README.md`
- 更新核心特点说明
- 添加智能分析策略说明
- 更新项目结构文档
- 更新文件功能描述

### 📊 使用示例

```bash
# 默认：昨天的文章，所有文章深度分析
./generate_digest.sh

# 指定日期：单日，所有文章深度分析
./generate_digest.sh -d 2026-02-15

# 多日窗口：如果 ≥10篇，则 Top 10 深度分析
./generate_digest.sh -d 2026-02-15 -w 48

# 多日窗口：如果 <10篇，则所有文章深度分析
./generate_digest.sh -d 2026-02-10 -w 72
```

### 🧪 测试结果

- ✅ 24h窗口（17篇）：所有文章深度分析 ✓
- ✅ 48h窗口（17篇）：Top 10深度分析 ✓
- ✅ Markdown报告标题动态生成 ✓
- ✅ HTML报告标题动态生成 ✓
- ✅ 元数据文件正确生成 ✓

### 🔧 技术细节

**判断逻辑**：
```python
if window_hours <= 24:
    # Rule 1: Single day - all articles
    return "all_single_day", article_count
elif article_count < 10:
    # Rule 2: Multi-day but less than 10 - all articles
    return "all_few", article_count
else:
    # Rule 3: Multi-day with 10+ articles - top 10
    return "top10", 10
```

**报告标题生成**：
```python
if mode in ["all_single_day", "all_few"]:
    title = "RSS 每日深度分析报告"
    desc = f"本报告包含 {total_articles} 篇文章的深度分析，..."
else:
    title = "RSS 深度分析报告 - Top 10 精选"
    desc = f"本报告从 {total_articles} 篇文章中精选了 Top {insight_count} 篇进行深度分析，..."
```

### 📝 数据流程

```
generate_digest.sh
    ↓ (传递 --window)
select_top10_and_insights.py
    ↓ (生成 insights_metadata.json)
generate_report.py
    ↓ (读取 metadata，生成动态标题)
digest_YYYY-MM-DD.md / .html
```

### 🎯 设计理念

1. **智能化**：自动根据场景选择最合适的策略
2. **灵活性**：支持单日和多日多种场景
3. **清晰性**：报告标题明确反映内容类型
4. **一致性**：保持现有工作流的兼容性

### ⚠️ 向后兼容性

- 所有现有功能保持不变
- 默认行为（昨天24h）仍然是所有文章深度分析
- 不需要修改现有的自动化脚本

---

**版本**: v2.1.0
**发布日期**: 2026-02-16
**状态**: ✅ 稳定版
