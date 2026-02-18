# RSS Digest 快速开始指南 🚀

5分钟快速配置并开始使用 RSS Digest。

## 📋 前置要求

- Python 3.7+
- Git（可选）
- 飞书企业账号（可选，用于团队协作）

## ⚡ 快速开始（3步）

### 1️⃣ 安装依赖

```bash
cd rss-digest
pip install -r rss-digest/scripts/requirements.txt
```

### 2️⃣ 生成第一份报告

```bash
./generate_digest.sh
```

就这么简单！脚本会：
- 解析RSS订阅源
- 抓取最近24小时的文章
- 生成AI摘要和洞察
- 创建Markdown和HTML报告
- 自动打开HTML报告

### 3️⃣ 查看报告

报告自动保存在 `output/` 目录：
- `digest_YYYY-MM-DD.md` - Markdown格式
- `digest_YYYY-MM-DD.html` - HTML格式（已自动打开）

## 📅 其他使用方式

```bash
# 生成指定日期的报告
./generate_digest.sh -d 2026-02-15

# 使用更大时间窗口（48小时）
./generate_digest.sh -w 48

# 生成上周的报告
./generate_digest.sh -w 168  # 7天
```

## 🔗 启用飞书集成（可选）

### 快速配置

```bash
# 1. 复制配置模板
cp .env.example .env

# 2. 编辑配置文件
vim .env
```

填入你的飞书凭证：
```bash
FEISHU_APP_ID=cli_xxxxxxxxxxxx
FEISHU_APP_SECRET=your_secret_here
FEISHU_MODE=create  # 创建模式（推荐）
```

### 测试连接

```bash
# 检查配置
./scripts/check_feishu_config.sh

# 测试连接
python3 scripts/test_feishu_connection.py
```

### 生成并上传

```bash
./generate_digest.sh
```

报告会自动上传到飞书根目录，你可以手动移动到任意文件夹。

## 📚 详细文档

### 飞书集成

- **新手指南**: [docs/FEISHU_QUICKSTART.md](docs/FEISHU_QUICKSTART.md)
- **完整指南**: [docs/FEISHU_INTEGRATION.md](docs/FEISHU_INTEGRATION.md)
- **模式说明**: [docs/FEISHU_MODES.md](docs/FEISHU_MODES.md)

### 项目文档

- **完整说明**: [README.md](README.md)
- **项目结构**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- **更新日志**: [CHANGELOG.md](CHANGELOG.md)
- **Skill定义**: [rss-digest/SKILL.md](rss-digest/SKILL.md)

## 🛠️ 常用命令

```bash
# 查看帮助
./generate_digest.sh -h

# 查看飞书配置
./scripts/check_feishu_config.sh

# 查看生成的报告
ls -lt output/

# 查看最新日志
ls -lt logs/ | head -5
```

## ❓ 遇到问题？

### 问题：没有找到文章

**解决**：增大时间窗口
```bash
./generate_digest.sh -d 2026-02-15 -w 48
```

### 问题：飞书上传失败

**解决**：检查配置和权限
```bash
./scripts/check_feishu_config.sh
python3 scripts/test_feishu_connection.py
```

### 问题：脚本执行很慢

**原因**：正常现象
- 抓取92个RSS源需要时间
- AI生成摘要和洞察需要人工交互
- 整个流程约需5-10分钟

## 🎯 下一步

1. **自定义RSS源**: 编辑 `rss-digest/opml/*.opml` 添加你的订阅
2. **配置飞书**: 按照上面的步骤配置飞书集成
3. **定时任务**: 设置cron或计划任务自动运行
4. **探索功能**: 查看完整文档了解高级功能

## 💡 提示

- **首次运行**会生成很多文章，可以使用 `-w 12` 缩小时间窗口
- **AI步骤**需要人工交互，脚本会打印提示
- **日志文件**保存在 `logs/` 目录，出错时查看
- **飞书根目录模式**最稳定，推荐使用

---

现在你已经掌握了基本用法！🎉

需要更多帮助？查看 [README.md](README.md) 或 [docs/](docs/) 目录下的详细文档。
