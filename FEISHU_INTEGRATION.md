# 飞书文档集成指南

本指南详细说明如何配置和使用RSS Digest的飞书（Lark）文档集成功能。

## 📋 目录

- [功能概述](#功能概述)
- [前置要求](#前置要求)
- [配置步骤](#配置步骤)
- [使用方法](#使用方法)
- [常见问题](#常见问题)
- [API说明](#api说明)

## 功能概述

飞书文档集成功能允许你：
- ✅ 自动将生成的markdown报告上传到飞书文档
- ✅ **每个报告创建独立的新文档**（不会覆盖已有文档）
- ✅ 在团队飞书空间中共享每日报告
- ✅ 通过URL快速访问和分享报告
- ✅ 在飞书云空间中长期保存历史报告
- ✅ 可选择将文档创建在指定文件夹下

## 前置要求

1. **飞书账号**: 需要有飞书企业账号
2. **应用权限**: 需要创建飞书应用或获得现有应用的凭证
3. **Python依赖**: 已安装 `requests` 和 `python-dotenv`

## 配置步骤

### 步骤 1: 创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/app/)
2. 点击「创建企业自建应用」
3. 填写应用名称和描述（如：RSS Digest Bot）
4. 创建完成后，记录 **App ID** 和 **App Secret**

### 步骤 2: 配置应用权限

在应用管理页面：

1. 进入「权限管理」
2. 搜索并开启以下权限：
   - `docx:document` - 创建、编辑、删除文档
   - `docx:document:readonly` - 查看文档
   - `drive:drive` - 访问云空间
   - `drive:drive:readonly` - 查看云空间（可选）

3. 点击「申请权限」并等待管理员审批（如果需要）

### 步骤 3: 获取文件夹Token（可选）

如果你想将报告上传到特定文件夹：

1. 在飞书云空间中打开目标文件夹
2. 查看URL，找到folder_token
   - URL格式: `https://xxx.feishu.cn/drive/folder/{folder_token}`
3. 记录这个 `folder_token`

### 步骤 4: 配置环境变量

在项目根目录：

```bash
# 复制配置模板
cp .env.example .env

# 编辑配置文件
vim .env  # 或使用其他编辑器
```

填入你的凭证：

```bash
# .env 文件内容
FEISHU_APP_ID=cli_xxxxxxxxxxxx
FEISHU_APP_SECRET=your_secret_here
FEISHU_FOLDER_TOKEN=FolderXXXXXX  # 可选
```

**重要提示**:
- 不要将 `.env` 文件提交到版本控制系统
- `.gitignore` 已包含 `.env` 的忽略规则
- 妥善保管你的 App Secret

## 使用方法

### 自动上传（推荐）

配置好环境变量后，直接运行生成脚本：

```bash
./generate_digest.sh
```

脚本会自动：
1. 生成本地报告
2. 检测飞书凭证
3. 上传到飞书文档
4. 保存飞书URL到本地

输出示例：
```
[Step 5/5] Generating reports...
✓ Reports generated successfully!

📤 Uploading to Feishu document...
Creating Feishu document: RSS Digest - digest_2026-02-18
Document created with token: doxcnXXXXXXXXXXXX
Writing content to document...
Content written successfully!
✓ Successfully uploaded to Feishu!
  URL: https://example.feishu.cn/docx/doxcnXXXXXXXXXXXX
```

### 手动上传

如果你已经生成了报告，可以单独上传：

```bash
# 使用环境变量
python3 rss-digest/scripts/upload_to_feishu.py output/digest_2026-02-18.md

# 指定文件夹
python3 rss-digest/scripts/upload_to_feishu.py output/digest_2026-02-18.md \
    --folder-token FolderXXXXXX

# 使用命令行凭证（不推荐，用于测试）
python3 rss-digest/scripts/upload_to_feishu.py output/digest_2026-02-18.md \
    --app-id cli_xxxxxxxxxxxx \
    --app-secret your_secret_here
```

### 查看飞书URL

上传成功后，URL会保存到：
```
output/digest_YYYY-MM-DD_feishu_url.txt
```

查看URL：
```bash
cat output/digest_2026-02-18_feishu_url.txt
```

## 常见问题

### Q1: 上传失败，提示"权限不足"

**解决方案**:
1. 检查应用权限配置是否正确
2. 确认权限审批已通过
3. 检查 App ID 和 App Secret 是否正确

### Q2: 找不到环境变量

**解决方案**:
1. 确认 `.env` 文件在项目根目录
2. 检查文件格式（每行一个变量，无空格）
3. 重新加载环境变量：`source .env`

### Q3: 文档内容显示不正确

**说明**: 当前版本使用简单的文本块上传，markdown格式可能不完全保留。

**改进建议**:
- 未来版本会实现更完善的markdown到飞书格式的转换
- 目前建议主要使用飞书文档作为归档和快速访问途径
- 需要完整格式时使用本地HTML报告

### Q6: 每次运行都会创建新文档吗？

**是的！** 这是设计行为：
- **每个报告创建独立文档** - 每次上传都会创建一个全新的飞书文档
- **不会覆盖已有文档** - 历史报告会被完整保留
- **便于版本管理** - 可以轻松对比不同日期的报告
- **支持文件夹整理** - 使用 `--folder-token` 参数将所有报告创建在同一文件夹下

**示例**:
```bash
# 2月15日的报告
./generate_digest.sh -d 2026-02-15  # → 创建文档A

# 2月16日的报告
./generate_digest.sh -d 2026-02-16  # → 创建文档B（不影响文档A）

# 2月17日的报告
./generate_digest.sh -d 2026-02-17  # → 创建文档C（不影响A和B）
```

### Q4: 想禁用飞书上传

**方案1**: 删除或重命名 `.env` 文件
```bash
mv .env .env.backup
```

**方案2**: 清空环境变量
```bash
unset FEISHU_APP_ID
unset FEISHU_APP_SECRET
```

**方案3**: 注释掉 `.env` 中的凭证
```bash
# FEISHU_APP_ID=cli_xxxxxxxxxxxx
# FEISHU_APP_SECRET=your_secret_here
```

### Q5: 批量上传历史报告

可以使用循环上传：

```bash
# 上传所有历史报告
for file in output/digest_*.md; do
    echo "Uploading $file..."
    python3 rss-digest/scripts/upload_to_feishu.py "$file"
    sleep 2  # 避免API限流
done
```

## API说明

### 飞书API端点

脚本使用以下飞书API：

1. **获取访问令牌**
   - 端点: `POST /open-apis/auth/v3/tenant_access_token/internal`
   - 用途: 获取临时访问令牌

2. **创建文档**
   - 端点: `POST /open-apis/docx/v1/documents`
   - 用途: 创建新的飞书文档

3. **写入内容**
   - 端点: `POST /open-apis/docx/v1/documents/{document_id}/blocks`
   - 用途: 向文档添加内容块

### 速率限制

飞书API有速率限制，建议：
- 单个应用：100次/分钟
- 批量上传时添加延迟（如上例中的 `sleep 2`）

### 文档格式

当前实现：
- 将markdown文本分块上传（每块最多5000字符）
- 使用文本块（block_type: 1）
- 保留原始markdown标记

## 高级配置

### 自定义文档标题

修改 `upload_to_feishu.py` 中的标题生成逻辑：

```python
# 原来的逻辑
title = f"RSS Digest - {filename}"

# 自定义标题
title = f"【每日资讯】{filename}"
```

### 添加文档描述

在创建文档时添加描述：

```python
data = {
    "title": title,
    "folder_token": folder_token,
    # 添加描述
    # "description": "AI生成的RSS每日深度报告"
}
```

### 配置超时时间

在请求中添加timeout参数：

```python
response = requests.post(url, headers=headers, json=data, timeout=30)
```

## 安全建议

1. **凭证管理**
   - 不要将凭证硬编码在脚本中
   - 不要提交 `.env` 文件到版本控制
   - 定期轮换 App Secret

2. **权限最小化**
   - 只开启必需的API权限
   - 使用独立的应用账号

3. **日志管理**
   - 检查日志文件，确保不包含敏感信息
   - 定期清理旧日志

## 反馈与支持

遇到问题？
- 查看日志文件: `logs/feishu_YYYY-MM-DD.log`
- 检查飞书开放平台文档: https://open.feishu.cn/document/
- 提交Issue到项目仓库

## 更新日志

### v1.3.0 (2026-02-18)
- ✅ 初始版本发布
- ✅ 支持自动上传到飞书文档
- ✅ 支持环境变量和命令行配置
- ✅ 集成到自动化工作流

---

**最后更新**: 2026-02-18
