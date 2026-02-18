# 更新日志 - Changelog

## v1.4.0 - 2026-02-18

### 🎉 飞书集成大幅增强

完全重构飞书集成，提供灵活的双模式支持和完整的诊断工具链。

### ✨ 新增功能

#### 1. **双模式飞书集成**
   - **追加模式 (Append Mode)** - 将所有报告追加到单一主文档
     - 便于集中管理和分享
     - 单一链接访问所有历史报告
     - 自动添加分隔符和时间戳
   - **创建模式 (Create Mode)** - 每次创建独立新文档
     - 独立文档便于归档
     - 支持根目录或指定文件夹
     - 灵活的文档组织

#### 2. **完整的诊断和测试工具**
   - `check_feishu_config.sh` - 查看当前配置状态
   - `test_feishu_connection.py` - 测试API连接和基本权限
   - `test_folder_permission.sh` - 测试文件夹创建权限
   - `grant_folder_permission.py` - 诊断和解决权限问题

#### 3. **增强的上传工具**
   - 新增 `upload_to_feishu_v2.py` 支持双模式
   - 自动分块上传大文件（>3000字符）
   - 智能错误处理和详细日志
   - 根目录模式（最可靠）和文件夹模式

#### 4. **完善的文档体系**
   - `docs/FEISHU_INTEGRATION.md` - 完整设置指南
   - `docs/FEISHU_MODES.md` - 模式对比和最佳实践
   - `docs/FEISHU_QUICKSTART.md` - 5分钟快速开始
   - `PROJECT_STRUCTURE.md` - 项目结构说明

### 🔧 改进

#### 1. **项目组织优化**
   - 创建 `docs/` 目录集中文档
   - 创建 `scripts/` 目录统一工具脚本
   - 创建 `archive/` 目录归档临时文件
   - 清理项目根目录结构

#### 2. **权限处理增强**
   - 自动检测和诊断权限问题
   - 清晰的错误信息和解决方案
   - 支持根目录模式避免权限复杂性
   - 详细的权限配置指南

#### 3. **配置管理改进**
   - 新增 `FEISHU_MODE` 配置项
   - 新增 `FEISHU_DOCUMENT_ID` 用于追加模式
   - 改进 `FEISHU_FOLDER_TOKEN` 说明
   - 配置验证和状态显示

### 🐛 修复

- 修复文件夹权限检测逻辑
- 修复长文本分块上传问题
- 修复API错误处理和重试机制
- 修复环境变量加载问题

### 📦 新增文件

**工具脚本**:
- `scripts/upload_to_feishu_v2.py` - 升级版上传工具
- `scripts/check_feishu_config.sh` - 配置检查工具
- `scripts/test_folder_permission.sh` - 权限测试工具
- `scripts/grant_folder_permission.py` - 权限诊断工具

**文档**:
- `docs/FEISHU_INTEGRATION.md` - 集成完整指南
- `docs/FEISHU_MODES.md` - 模式说明文档
- `docs/FEISHU_QUICKSTART.md` - 快速开始指南
- `PROJECT_STRUCTURE.md` - 项目结构文档

### 🔄 更新文件

- `rss-digest/SKILL.md` - 更新到 v1.4，完整功能说明
- `generate_digest.sh` - 使用新版上传工具
- `.env.example` - 添加新配置项
- `README.md` - 更新飞书集成说明

### 💡 使用建议

**日常使用推荐配置**:
```bash
FEISHU_MODE=create  # 创建模式
# FEISHU_FOLDER_TOKEN 注释掉，使用根目录
```

**原因**:
- 根目录创建最稳定可靠
- 避免复杂的文件夹权限配置
- 可手动移动文档到任意文件夹
- 测试验证完全通过

---

## v1.3.0 - 2026-02-18

### 🚀 飞书文档集成

为RSS Digest添加了飞书（Lark）文档集成功能，支持将每日报告自动上传到飞书文档，方便团队协作和分享。

### ✨ 新增功能

1. **飞书文档自动上传**
   - 新增 `upload_to_feishu.py` 脚本
   - 支持通过飞书API创建文档并上传markdown内容
   - 自动保存飞书文档URL到本地文件

2. **灵活的凭证配置**
   - 支持环境变量配置（推荐）
   - 支持命令行参数配置
   - 新增 `.env.example` 配置模板
   - 可选的文件夹指定功能

3. **集成到自动化工作流**
   - `generate_digest.sh` 自动检测飞书凭证
   - 如已配置则自动上传，否则跳过（不影响本地报告生成）
   - 上传日志保存到 `logs/feishu_YYYY-MM-DD.log`

### 📦 新增文件

- `scripts/upload_to_feishu.py` - 飞书文档上传脚本
- `.env.example` - 环境变量配置模板

### 🔄 改进的文件

#### 1. `generate_digest.sh`
- 添加飞书上传步骤（可选）
- 检测环境变量 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET`
- 上传成功后显示飞书文档URL

#### 2. `scripts/requirements.txt`
- 添加 `requests>=2.31.0` - HTTP请求库
- 添加 `python-dotenv>=1.0.0` - 环境变量管理

#### 3. `rss-digest/SKILL.md`
- 版本更新到 v1.3
- 添加飞书集成设置说明
- 添加手动上传使用示例
- 更新功能列表和概览

#### 4. `README.md`
- 添加飞书集成配置说明
- 更新项目结构（新增飞书相关文件）
- 添加手动上传使用示例
- 更新核心特点列表

### 🎯 使用场景

- **团队协作**: 自动将每日报告上传到团队的飞书空间
- **远程访问**: 通过飞书URL在任何设备上查看报告
- **长期归档**: 在飞书云空间中保存历史报告
- **快速分享**: 一键分享飞书文档链接给同事

### 📝 升级说明

对于现有用户：
1. 更新依赖：`pip install -r rss-digest/scripts/requirements.txt`
2. （可选）配置飞书凭证：`cp .env.example .env` 并填写
3. 继续使用 `./generate_digest.sh`，脚本会自动检测并使用飞书功能

**注意**: 飞书集成是完全可选的。如不配置飞书凭证，脚本仍会正常生成本地markdown和HTML报告。

---

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
