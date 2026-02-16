# Findings

## Key Discoveries
- fetch_rss.py 的 --date 参数定义了但从未使用，导致日期过滤无效
- generate_report.py 使用 datetime.now() 而不是文章日期作为报告标题
- 当 selection_mode="all" 时，报告不会显示全部资讯概要

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| IndentationError: unexpected indent | 2次 | 修复 if 语句后的缩进 |
| 抓取 2.14 日文章却包含 2.13 日 | 1次 | 修复 fetch_rss.py 日期过滤逻辑 |

## Decisions Made
- 选择修复 fetch_rss.py 而非重写：改动最小，风险最低
- 选择修复 generate_report.py：使用文章实际日期而非当前日期
- 选择始终显示全部资讯概要：提升用户体验

## Code Changes
- `rss-digest/scripts/fetch_rss.py`: 添加 target_date 参数支持
- `rss-digest/scripts/generate_report.py`: 添加 date_str 参数
- `rss-digest/assets/report_template_v2.html`: 更新标题文本
