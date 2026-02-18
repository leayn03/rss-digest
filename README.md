# RSS Daily Deep Insight Report - RSS 每日深度分析报告

AI驱动的RSS资讯深度分析系统，智能抓取指定日期的文章，并根据时间窗口和文章数量自动选择最合适的分析策略。

## ✨ 核心特点

- ✅ **日期配置化**：默认抓取昨天的文章，支持指定任意日期
- ✅ **智能深度分析**：根据时间窗口和文章数量自动选择分析策略
  - 单日/昨天（≤24h）→ 所有文章深度分析
  - 多日 + <10篇 → 所有文章深度分析
  - 多日 + ≥10篇 → Top 10深度分析
- ✅ **200字智能摘要**：AI生成每篇文章的中文摘要
- ✅ **精美双格式报告**：Markdown + HTML（带交互式标签筛选）
- ✅ **完整工作流自动化**：一键运行全流程
- ✅ **灵活时间窗口**：可配置文章时间范围（默认24小时）
- 🆕 **飞书文档集成**：自动上传报告到飞书文档，方便团队协作

## 📊 项目结构

```
rss-digest/
├── README.md                       # 项目说明
├── RSS_DIGEST_WORKFLOW.md          # 详细工作流程文档
├── generate_digest.sh              # 一键生成脚本
├── .gitignore                      # Git忽略配置
├── data/                           # 数据文件目录
│   ├── feeds.json                  # RSS源列表
│   ├── articles_raw.json           # 原始抓取的文章
│   ├── articles.json               # 带AI摘要的文章
│   ├── insights_metadata.json      # 洞察选择策略元数据
│   └── insights.json               # 深度洞察
├── logs/                           # 日志文件目录
│   ├── parse_YYYY-MM-DD.log        # OPML解析日志
│   ├── fetch_YYYY-MM-DD.log        # RSS抓取日志
│   ├── summaries_YYYY-MM-DD.log    # AI摘要生成日志
│   ├── insights_YYYY-MM-DD.log     # 洞察生成日志
│   ├── report_YYYY-MM-DD.log       # 报告生成日志
│   └── feishu_YYYY-MM-DD.log       # 飞书上传日志
├── output/                         # 生成的报告
│   ├── digest_YYYY-MM-DD.md        # Markdown报告
│   ├── digest_YYYY-MM-DD.html      # HTML报告
│   └── digest_YYYY-MM-DD_feishu_url.txt  # 飞书文档URL
└── rss-digest/                     # 核心代码
    ├── opml/                       # OPML订阅文件
    │   └── hn-popular-blogs-2025.opml
    ├── scripts/                    # Python脚本
    │   ├── parse_opml.py           # 解析OPML
    │   ├── fetch_rss.py            # 抓取RSS（可配置时间窗口）
    │   ├── generate_summaries.py   # 生成AI摘要
    │   ├── select_top10_and_insights.py  # 智能选择深度分析文章
    │   ├── generate_report.py      # 生成智能报告
    │   ├── upload_to_feishu.py     # 上传到飞书文档
    │   └── requirements.txt        # 依赖包
    └── assets/                     # 资源文件
        ├── report_template.html    # 基础HTML模板
        └── report_template_v2.html # 增强版HTML模板（带标签筛选）
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd rss-digest
pip install -r rss-digest/scripts/requirements.txt
```

依赖包括：
- `feedparser` - RSS feed解析
- `python-dateutil` - 日期处理
- `requests` - HTTP请求（飞书API）
- `python-dotenv` - 环境变量管理

### 2. 配置飞书集成（可选）

如需将报告自动上传到飞书文档：

1. 访问 [飞书开放平台](https://open.feishu.cn/app/) 创建应用
2. 获取 **App ID** 和 **App Secret**
3. 配置应用权限：`docx:document`（文档读写）、`drive:drive`（云空间访问）
4. 复制配置模板并填写凭证：

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的凭证
```

5. **测试连接**（推荐）：

```bash
python3 rss-digest/scripts/test_feishu_connection.py
```

这会验证你的凭证是否正确，并创建一个测试文档。

**注意**：
- 如果不配置飞书凭证，脚本仍会正常生成本地报告，只是跳过飞书上传步骤
- **每个报告创建独立文档** - 不会覆盖已有文档，所有历史报告都会保留

### 3. 运行完整工作流

```bash
# 默认：抓取昨天的文章
./generate_digest.sh

# 指定日期
./generate_digest.sh -d 2026-02-15

# 使用更宽的时间窗口（48小时）
./generate_digest.sh -w 48

# 查看帮助
./generate_digest.sh -h
```

**工作流程**：
1. 解析OPML文件提取RSS源（92个）
2. 抓取指定日期的文章（默认昨天，24小时窗口）
3. 为所有文章生成200字AI摘要
4. 生成深度洞察提示词（需要Claude AI）
5. 生成精美的Markdown和HTML报告
6. 🆕 **自动上传到飞书文档（如已配置）**
7. 自动打开HTML报告

所有日志文件会自动保存到 `logs/` 目录。

### 3. 手动运行（分步执行）

如需手动控制每个步骤：

```bash
# Step 1: 解析OPML
python3 rss-digest/scripts/parse_opml.py rss-digest/opml/hn-popular-blogs-2025.opml > data/feeds.json

# Step 2: 抓取文章（默认昨天）
python3 rss-digest/scripts/fetch_rss.py data/feeds.json > data/articles_raw.json

# 或指定日期
python3 rss-digest/scripts/fetch_rss.py data/feeds.json --date 2026-02-15 > data/articles_raw.json

# Step 3: 生成AI摘要（200字）
python3 rss-digest/scripts/generate_summaries.py

# Step 4: 生成深度洞察提示词
python3 rss-digest/scripts/select_top10_and_insights.py
# 将输出的提示词发送给Claude，获取insights JSON，保存到 data/insights.json

# Step 5: 生成报告
python3 rss-digest/scripts/generate_report.py data/articles.json data/insights.json output/

# Step 6: 上传到飞书（可选）
python3 rss-digest/scripts/upload_to_feishu.py output/digest_$(date +%Y-%m-%d).md

# Step 7: 打开报告
open output/digest_$(date +%Y-%m-%d).html
```

### 4. 手动上传到飞书

如果你已经生成了报告，可以单独上传到飞书：

```bash
# 使用环境变量中的凭证（推荐）
python3 rss-digest/scripts/upload_to_feishu.py output/digest_2026-02-17.md

# 上传到指定文件夹
python3 rss-digest/scripts/upload_to_feishu.py output/digest_2026-02-17.md \
    --folder-token FolderXXXXXX

# 通过命令行提供凭证
python3 rss-digest/scripts/upload_to_feishu.py output/digest_2026-02-17.md \
    --app-id cli_xxxxxxxxxxxx \
    --app-secret your_secret_here
```

上传成功后，脚本会：
- 打印飞书文档URL
- 将URL保存到 `output/digest_YYYY-MM-DD_feishu_url.txt`

## 📝 配置说明

### 修改抓取日期

```bash
# 默认抓取昨天的文章
./generate_digest.sh

# 指定具体日期
./generate_digest.sh -d 2026-02-15
```

### 修改时间窗口

```bash
# 默认24小时窗口（昨天中午前后12小时）
./generate_digest.sh

# 使用48小时窗口（适合文章较少的情况）
./generate_digest.sh -w 48

# 指定日期 + 自定义窗口
./generate_digest.sh -d 2026-02-15 -w 36
```

### 添加新的RSS源

1. 使用RSS阅读器导出OPML文件
2. 替换 `rss-digest/opml/hn-popular-blogs-2025.opml`
3. 重新运行 `./generate_digest.sh`

## 🎨 HTML报告特色

**RSS 每日深度分析报告** 包含以下特色：

1. **全文深度洞察**
   - 每篇文章均配有1000字深度分析
   - 完整的Markdown格式支持（标题、列表、代码块等）
   - 清晰的视觉层次和排版

2. **交互式标签筛选**
   - 点击顶部筛选标签快速过滤文章
   - 支持按来源、分类筛选

3. **精美设计**
   - 渐变色背景和卡片设计
   - 文章编号徽章
   - 响应式布局，完美支持移动设备

4. **完整的文章信息**
   - 标题、链接、来源、分类、发布时间
   - 200字AI摘要
   - 1000字深度洞察
   - 可点击的标签

## 🤖 AI分析流程

### 1. 文章摘要生成（200字）

为**所有文章**生成中文摘要，重点包括：
- 核心观点和技术要点
- 实践价值和启发
- 与当前技术趋势的关联

### 2. 智能深度洞察生成（1000字）

系统根据以下规则自动选择分析策略：

**规则1：单日模式（时间窗口 ≤ 24小时）**
- 为**所有文章**生成深度洞察
- 适用场景：默认的昨天模式，或指定单一日期
- 报告标题：《RSS 每日深度分析报告》

**规则2：多日少量模式（时间窗口 > 24小时 且 文章 < 10篇）**
- 为**所有文章**生成深度洞察
- 适用场景：使用较宽时间窗口但文章数量较少
- 报告标题：《RSS 每日深度分析报告》

**规则3：多日精选模式（时间窗口 > 24小时 且 文章 ≥ 10篇）**
- 只为**Top 10文章**生成深度洞察
- 其他文章仍有200字摘要
- 报告标题：《RSS 深度分析报告 - Top 10 精选》

深度洞察包括：
- 核心观点的深入解读
- 技术细节和实现原理
- 行业背景和趋势分析
- 实践启示和应用价值
- 延伸思考和讨论问题

### 3. 智能化程度

- **自动化部分**：RSS抓取、OPML解析、策略选择、报告生成
- **AI辅助部分**：摘要生成、深度洞察生成（需要Claude）
- 可以通过Claude API实现完全自动化

## 🔄 自动化设置

### 每日定时任务

创建cron job，每天早上8点自动生成昨天的深度分析报告：

```bash
crontab -e

# 添加以下行（默认会抓取昨天的文章）
0 8 * * * cd /Users/leayn/Documents/PythonProject/rss-digest && ./generate_digest.sh >> logs/cron.log 2>&1
```

### 使用launchd（macOS推荐）

创建 `~/Library/LaunchAgents/com.user.rss-digest.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.rss-digest</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/leayn/Documents/PythonProject/rss-digest/generate_digest.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/leayn/Documents/PythonProject/rss-digest/logs/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/leayn/Documents/PythonProject/rss-digest/logs/launchd-error.log</string>
</dict>
</plist>
```

激活任务：
```bash
launchctl load ~/Library/LaunchAgents/com.user.rss-digest.plist
```

## 📚 详细文档

- [RSS_DIGEST_WORKFLOW.md](RSS_DIGEST_WORKFLOW.md) - 完整工作流程和故障排除
- [rss-digest/SKILL.md](rss-digest/SKILL.md) - Skill详细说明

## 🛠️ 故障排除

### 问题1: 没有抓取到文章

**可能原因**:
1. 指定日期没有文章发布
2. 时间窗口太窄
3. 网络连接问题

**解决**:
```bash
# 使用更宽的时间窗口
./generate_digest.sh -d 2026-02-15 -w 48

# 检查日志
cat logs/fetch_2026-02-15.log
```

### 问题2: SSL证书错误

**症状**: `certificate verify failed`

**解决**: 代码已包含SSL修复（在`fetch_rss.py`中）

### 问题3: HTML报告样式异常

**解决**: 确保使用 `report_template_v2.html` 模板，并已安装 `markdown` 库

### 问题4: 深度洞察未生成

**原因**: 需要手动使用Claude生成洞察

**解决**:
1. 运行 `python3 rss-digest/scripts/select_top10_and_insights.py`
2. 将输出的提示词发送给Claude
3. 将Claude返回的JSON保存到 `data/insights.json`
4. 重新运行 `./generate_digest.sh`

## 📊 示例数据

典型运行统计：
- RSS源：92个
- 目标日期：昨天（可配置）
- 时间窗口：24小时（可配置）
- 获取文章：10-50篇（视当天更新情况）
- AI摘要：每篇 200字
- 深度洞察：每篇 1000字
- 总字数：约 15,000 - 60,000 字（取决于文章数量）

## 📄 License

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

**生成日期**: 2026-02-16
**版本**: 2.0
