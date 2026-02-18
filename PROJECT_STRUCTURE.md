# RSS Digest 项目结构

本文档描述 RSS Digest 项目的目录结构和文件组织。

## 📁 目录结构

```
rss-digest/
├── 📄 核心文件
│   ├── generate_digest.sh          # 主运行脚本
│   ├── .env                        # 配置文件（飞书凭证）
│   ├── .env.example                # 配置模板
│   └── README.md                   # 项目说明
│
├── 📂 rss-digest/                  # Python 核心模块
│   ├── scripts/                    # Python 脚本
│   │   ├── parse_opml.py          # 解析 OPML 文件
│   │   ├── fetch_rss.py           # 抓取 RSS 文章
│   │   ├── generate_summaries.py  # 生成 AI 摘要
│   │   ├── generate_insights.py   # 生成深度洞察
│   │   └── generate_report.py     # 生成最终报告
│   ├── opml/                       # RSS 订阅源
│   │   └── *.opml
│   └── SKILL.md                    # Skill 定义文档
│
├── 📂 scripts/                     # 工具脚本
│   ├── upload_to_feishu_v2.py     # 飞书上传工具（推荐）
│   ├── upload_to_feishu.py        # 飞书上传工具（旧版）
│   ├── test_feishu_connection.py  # 测试飞书连接
│   ├── test_folder_permission.sh  # 测试文件夹权限
│   ├── check_feishu_config.sh     # 查看飞书配置
│   └── grant_folder_permission.py # 诊断文件夹权限
│
├── 📂 docs/                        # 文档目录
│   ├── FEISHU_INTEGRATION.md      # 飞书集成完整指南
│   ├── FEISHU_MODES.md            # 飞书模式说明
│   └── FEISHU_QUICKSTART.md       # 飞书快速开始
│
├── 📂 output/                      # 生成的报告
│   ├── digest_YYYY-MM-DD.md       # Markdown 报告
│   ├── digest_YYYY-MM-DD.html     # HTML 报告
│   └── digest_YYYY-MM-DD_feishu_url.txt  # 飞书链接
│
├── 📂 data/                        # 临时数据
│   ├── feeds.json                 # 解析后的 RSS 源
│   ├── articles_raw.json          # 原始文章数据
│   ├── articles.json              # 带摘要的文章
│   └── insights.json              # 深度洞察数据
│
├── 📂 logs/                        # 日志文件
│   ├── parse_YYYY-MM-DD.log
│   ├── fetch_YYYY-MM-DD.log
│   ├── summaries_YYYY-MM-DD.log
│   ├── insights_YYYY-MM-DD.log
│   ├── report_YYYY-MM-DD.log
│   └── feishu_YYYY-MM-DD.log
│
└── 📂 archive/                     # 归档文件
    └── *.md                        # 临时/过时文档

```

## 📝 文件说明

### 核心脚本

#### generate_digest.sh
主运行脚本，完整的工作流程：
1. 解析 OPML 文件
2. 抓取 RSS 文章
3. 生成 AI 摘要
4. 生成深度洞察
5. 生成 Markdown/HTML 报告
6. 上传到飞书（可选）

```bash
# 使用示例
./generate_digest.sh              # 生成昨天的报告
./generate_digest.sh -d 2026-02-15  # 指定日期
./generate_digest.sh -w 48        # 48小时窗口
```

### 配置文件

#### .env
存储敏感配置信息：
- `FEISHU_APP_ID` - 飞书应用 ID
- `FEISHU_APP_SECRET` - 飞书应用密钥
- `FEISHU_MODE` - 工作模式（append/create）
- `FEISHU_DOCUMENT_ID` - 追加模式目标文档
- `FEISHU_FOLDER_TOKEN` - 创建模式目标文件夹

**注意**：不要提交 .env 到版本控制！

### Python 核心模块

#### rss-digest/scripts/
- `parse_opml.py` - 解析 OPML 订阅文件
- `fetch_rss.py` - 抓取 RSS 文章，支持日期过滤
- `generate_summaries.py` - 调用 AI 生成 200 字摘要
- `generate_insights.py` - 生成 1000 字深度洞察
- `generate_report.py` - 汇总生成 Markdown/HTML 报告

### 工具脚本

#### scripts/upload_to_feishu_v2.py ⭐
推荐使用的飞书上传工具，支持：
- 追加模式（append）- 追加到现有文档
- 创建模式（create）- 创建新文档
- 自动分块上传
- 根目录或指定文件夹

```bash
python3 scripts/upload_to_feishu_v2.py output/digest_2026-02-17.md
```

#### scripts/check_feishu_config.sh
快速查看当前飞书配置状态：
```bash
./scripts/check_feishu_config.sh
```

#### scripts/test_feishu_connection.py
测试飞书 API 连接和基本权限：
```bash
python3 scripts/test_feishu_connection.py
```

#### scripts/test_folder_permission.sh
测试文件夹创建权限：
```bash
./scripts/test_folder_permission.sh
```

### 文档目录

#### docs/FEISHU_INTEGRATION.md
飞书集成完整指南，包含：
- 功能概述
- 前置要求
- 详细配置步骤
- 常见问题解答
- API 说明

#### docs/FEISHU_MODES.md
两种工作模式的详细说明：
- 追加模式（append）
- 创建模式（create）
- 模式切换方法
- 最佳实践

#### docs/FEISHU_QUICKSTART.md
5分钟快速开始指南

### 输出文件

#### output/
生成的报告文件：
- `digest_YYYY-MM-DD.md` - Markdown 格式
- `digest_YYYY-MM-DD.html` - HTML 格式（带样式）
- `digest_YYYY-MM-DD_feishu_url.txt` - 飞书文档链接

### 数据目录

#### data/
存储处理过程中的临时数据：
- `feeds.json` - 解析后的 RSS 源列表
- `articles_raw.json` - 原始文章（仅标题、链接、时间）
- `articles.json` - 带 AI 摘要的文章
- `insights.json` - 深度洞察内容

**注意**：data/ 目录包含在 .gitignore 中

### 日志目录

#### logs/
每个步骤的详细日志，按日期命名：
- `parse_*.log` - OPML 解析日志
- `fetch_*.log` - RSS 抓取日志
- `summaries_*.log` - 摘要生成日志
- `insights_*.log` - 洞察生成日志
- `report_*.log` - 报告生成日志
- `feishu_*.log` - 飞书上传日志

## 🔄 工作流程

```
1. 解析 OPML
   └─> feeds.json

2. 抓取 RSS
   └─> articles_raw.json

3. 生成摘要
   └─> articles.json

4. 生成洞察
   └─> insights.json

5. 生成报告
   └─> digest_*.md + digest_*.html

6. 上传飞书（可选）
   └─> 飞书文档 + *_feishu_url.txt
```

## 🚀 快速开始

### 1. 初始配置
```bash
# 复制配置模板
cp .env.example .env

# 编辑配置文件
vim .env
```

### 2. 测试飞书连接
```bash
python3 scripts/test_feishu_connection.py
```

### 3. 生成报告
```bash
./generate_digest.sh
```

## 📋 维护指南

### 添加新的 RSS 源
编辑 `rss-digest/opml/*.opml` 文件，添加新的 RSS 订阅。

### 查看日志
```bash
# 查看最新日志
ls -lt logs/ | head -5

# 查看特定日志
tail -f logs/fetch_2026-02-17.log
```

### 清理旧数据
```bash
# 清理 data 目录
rm -rf data/*.json

# 清理旧日志（保留最近7天）
find logs/ -name "*.log" -mtime +7 -delete

# 清理旧报告（保留最近30天）
find output/ -name "digest_*" -mtime +30 -delete
```

## 🔧 故障排查

### 问题：生成报告失败
1. 检查日志文件：`ls -lt logs/ | head`
2. 查看错误：`cat logs/fetch_*.log`

### 问题：飞书上传失败
1. 检查配置：`./scripts/check_feishu_config.sh`
2. 测试连接：`python3 scripts/test_feishu_connection.py`
3. 查看日志：`cat logs/feishu_*.log`

### 问题：抓取文章数量为 0
1. 检查日期是否正确
2. 增大时间窗口：`./generate_digest.sh -w 48`
3. 检查 RSS 源是否可访问

## 🔒 安全注意事项

1. **不要提交 .env 文件**
   - 已在 .gitignore 中排除
   - 包含敏感的 API 凭证

2. **妥善保管凭证**
   - 定期轮换 App Secret
   - 不要在日志中输出凭证

3. **最小权限原则**
   - 只开启必需的 API 权限
   - 使用独立的应用账号

## 📚 相关文档

- [README.md](../README.md) - 项目主文档
- [CHANGELOG.md](../CHANGELOG.md) - 更新日志
- [docs/FEISHU_INTEGRATION.md](docs/FEISHU_INTEGRATION.md) - 飞书集成指南
- [rss-digest/SKILL.md](rss-digest/SKILL.md) - Skill 定义

---

**最后更新**: 2026-02-18
