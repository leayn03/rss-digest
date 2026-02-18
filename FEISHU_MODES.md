# 飞书集成模式说明

RSS Digest 支持两种飞书文档集成模式，通过 `.env` 配置文件切换。

## 📋 两种工作模式

### 模式 1: 追加模式 (Append Mode) ⭐ 推荐

**特点**：将每日报告追加到同一个文档中，便于集中管理

**使用场景**：
- ✅ 想在一个文档中查看所有历史报告
- ✅ 便于分享单个文档链接
- ✅ 减少文档数量，便于管理

**配置方法**：

```bash
# .env 文件配置
FEISHU_MODE=append
FEISHU_DOCUMENT_ID=BFf2dweffoJleixPUcscchUynNg  # 您的目标文档ID
```

**文档ID获取方法**：
1. 在飞书中创建或打开一个文档
2. 从URL中获取文档ID：
   ```
   https://xxx.feishu.cn/docx/{DOCUMENT_ID}
                                ^^^^^^^^^ 这部分就是文档ID
   ```
3. 将文档ID填入 `.env` 的 `FEISHU_DOCUMENT_ID`

**效果**：
- 每次运行自动追加到指定文档末尾
- 报告之间有分隔线
- 每个报告有日期标题和时间戳
- 所有历史报告保存在同一文档中

---

### 模式 2: 创建模式 (Create Mode)

**特点**：每次生成报告时创建独立的新文档

**使用场景**：
- ✅ 每日报告需要独立存档
- ✅ 需要灵活移动和组织文档
- ✅ 便于删除单个日期的报告

**配置方法**：

```bash
# .env 文件配置
FEISHU_MODE=create
FEISHU_FOLDER_TOKEN=Pz1wfydIglHWBhdFmAicScuCn6e  # 可选：指定文件夹
```

**文件夹Token获取方法**（可选）：
1. 在飞书云空间中创建一个文件夹（如"RSS每日报告"）
2. 打开文件夹，从URL中获取token：
   ```
   https://xxx.feishu.cn/drive/folder/{FOLDER_TOKEN}
                                       ^^^^^^^^^^^^ 这部分就是文件夹Token
   ```
3. 将token填入 `.env` 的 `FEISHU_FOLDER_TOKEN`

**效果**：
- 每次运行创建新文档
- 标题格式：`RSS Digest - 2026-02-17`
- 如果配置了文件夹，文档创建在指定文件夹下
- 如果未配置文件夹，文档创建在根目录

---

## 🔄 模式切换

### 从创建模式切换到追加模式

1. 编辑 `.env` 文件：
```bash
FEISHU_MODE=append  # 改为 append
FEISHU_DOCUMENT_ID=YOUR_DOC_ID  # 添加文档ID
```

2. 运行测试：
```bash
./generate_digest.sh -d 2026-02-17
```

3. 检查文档，确认内容已追加

### 从追加模式切换到创建模式

1. 编辑 `.env` 文件：
```bash
FEISHU_MODE=create  # 改为 create
FEISHU_FOLDER_TOKEN=YOUR_FOLDER_TOKEN  # 可选：指定文件夹
```

2. 运行测试：
```bash
./generate_digest.sh -d 2026-02-16
```

3. 检查飞书，确认创建了新文档

---

## 🛠️ 配置文件示例

### 完整的 .env 配置示例

```bash
# 飞书应用凭证
FEISHU_APP_ID=cli_xxxxxxxxxxxx
FEISHU_APP_SECRET=your_secret_here

# 选择工作模式 (append 或 create)
FEISHU_MODE=append

# 追加模式配置
FEISHU_DOCUMENT_ID=BFf2dweffoJleixPUcscchUynNg

# 创建模式配置（如果使用创建模式，注释掉上面的DOCUMENT_ID）
# FEISHU_FOLDER_TOKEN=Pz1wfydIglHWBhdFmAicScuCn6e
```

---

## 📝 使用说明

### 日常使用

无论哪种模式，使用方法都一样：

```bash
# 生成昨天的报告
./generate_digest.sh

# 生成指定日期的报告
./generate_digest.sh -d 2026-02-15

# 生成更大时间窗口的报告
./generate_digest.sh -d 2026-02-15 -w 48
```

报告会根据 `.env` 中的配置自动上传到飞书。

### 手动上传

如果需要手动上传已生成的报告：

```bash
# 使用 .env 中的配置
python3 scripts/upload_to_feishu_v2.py output/digest_2026-02-17.md

# 查看上传日志
cat logs/feishu_2026-02-17.log
```

---

## 🔍 查看上传结果

### 追加模式

访问您配置的文档：
```
https://ecnjqkm7hoqs.feishu.cn/docx/{FEISHU_DOCUMENT_ID}
```

### 创建模式

查看保存的URL：
```bash
cat output/digest_2026-02-17_feishu_url.txt
```

或查看上传日志：
```bash
tail logs/feishu_2026-02-17.log
```

---

## ❓ 常见问题

### Q1: 如何切换我的飞书域名？

修改脚本中的域名（如果默认域名无法访问）：

编辑 `scripts/upload_to_feishu_v2.py`，将 `ecnjqkm7hoqs.feishu.cn` 替换为您的域名。

### Q2: 追加模式下文档太长怎么办？

当文档变得很长时，可以：
1. 创建新文档，更新 `FEISHU_DOCUMENT_ID`
2. 或切换到创建模式
3. 或手动归档旧内容

### Q3: 能否同时使用两种模式？

不能同时使用，但可以灵活切换：
- 每月第一天切换到创建模式，创建本月文档
- 更新 `FEISHU_DOCUMENT_ID` 为新文档
- 继续使用追加模式

### Q4: 权限配置

确保飞书应用有以下权限：
- ✅ `docx:document` - 创建、编辑文档
- ✅ `drive:drive` - 访问云空间

确保应用有目标文档/文件夹的访问权限：
1. 打开目标文档或文件夹
2. 点击「共享」
3. 添加应用（如：RSS Digest Bot）
4. 授予「可编辑」权限

---

## 📊 模式对比

| 特性 | 追加模式 | 创建模式 |
|-----|---------|---------|
| 文档数量 | 1个文档包含所有报告 | 每个报告独立文档 |
| 便于分享 | ✅ 单个链接 | ❌ 需要多个链接 |
| 便于管理 | ✅ 集中管理 | ❌ 需要整理 |
| 灵活性 | ❌ 难以删除单日 | ✅ 可独立操作 |
| 文档长度 | ⚠️ 会越来越长 | ✅ 每个文档短小 |
| 推荐场景 | 日常使用 | 特殊归档 |

---

## 🎯 最佳实践

### 推荐配置（追加模式）

1. 创建一个专门的飞书文档，命名为"RSS每日报告汇总"
2. 配置追加模式，使用这个文档ID
3. 每月初创建新文档，更新配置
4. 旧文档归档保存

### 文档组织建议

```
📁 RSS每日报告/
  📄 2026-02 RSS汇总（追加模式文档）
  📄 2026-01 RSS汇总（归档）
  📄 2025-12 RSS汇总（归档）
```

---

**最后更新**: 2026-02-18
