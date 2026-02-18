# 飞书集成快速开始 🚀

5分钟快速配置飞书文档自动上传功能。

## ⚡ 快速配置（3步）

### 1️⃣ 创建飞书应用

访问 https://open.feishu.cn/app/ 并：
- 点击「创建企业自建应用」
- 填写名称：`RSS Digest Bot`
- 记录 **App ID** 和 **App Secret**

### 2️⃣ 配置权限

在应用管理页面 → 「权限管理」：
- ✅ 搜索并开启 `docx:document`
- ✅ 搜索并开启 `drive:drive`
- 💡 等待管理员审批（如需要）

### 3️⃣ 配置凭证

```bash
cd rss-digest
cp .env.example .env
vim .env  # 填入你的凭证
```

`.env` 文件内容：
```bash
FEISHU_APP_ID=cli_xxxxxxxxxxxx
FEISHU_APP_SECRET=your_secret_here
FEISHU_FOLDER_TOKEN=FolderXXXXXX  # 可选
```

## 🧪 测试连接

```bash
python3 rss-digest/scripts/test_feishu_connection.py
```

看到 ✅ 表示配置成功！

## 🎉 开始使用

```bash
./generate_digest.sh
```

报告会自动：
1. 生成本地 Markdown 和 HTML
2. 上传到飞书文档（新建文档）
3. 打印飞书文档URL
4. 保存URL到 `output/digest_YYYY-MM-DD_feishu_url.txt`

## 📌 重要说明

### ✅ 每个报告创建独立文档

```bash
./generate_digest.sh -d 2026-02-15  # → 创建文档A
./generate_digest.sh -d 2026-02-16  # → 创建文档B
./generate_digest.sh -d 2026-02-17  # → 创建文档C
```

**不会覆盖！** 每次都是新文档，历史报告完整保留。

### 📁 使用文件夹整理

在飞书云空间创建文件夹（如"RSS每日报告"），获取folder_token：

1. 打开文件夹，查看URL
2. 找到 `folder/{token}` 部分
3. 将token填入 `.env`：

```bash
FEISHU_FOLDER_TOKEN=FolderXXXXXXXXXX
```

这样所有报告都会创建在该文件夹下。

### 🔗 获取文档URL

上传成功后：
```bash
# 查看保存的URL
cat output/digest_2026-02-18_feishu_url.txt

# 或从上传日志中查看
tail logs/feishu_2026-02-18.log
```

## 🆘 常见问题

### ❌ 权限不足

检查：
1. 应用权限是否已开启
2. 是否等待了管理员审批
3. 凭证是否正确

### ❌ 创建文档失败

确认：
1. 网络连接正常
2. App ID和Secret正确（复制时没有多余空格）
3. 应用未被禁用

### ❌ URL无法访问

飞书文档URL格式：
```
https://{租户域名}.feishu.cn/docx/{doc_id}
```

替换 `{租户域名}` 为你的实际域名：
- bytedance.feishu.cn
- xxx.feishu.cn
- xxx.larksuite.com

## 📖 详细文档

需要更多信息？查看：
- [FEISHU_INTEGRATION.md](FEISHU_INTEGRATION.md) - 完整配置指南
- [README.md](README.md) - 项目主文档

## 🔧 高级用法

### 手动上传单个文件

```bash
python3 rss-digest/scripts/upload_to_feishu.py output/digest_2026-02-17.md
```

### 批量上传历史报告

```bash
for file in output/digest_*.md; do
    echo "上传 $file..."
    python3 rss-digest/scripts/upload_to_feishu.py "$file"
    sleep 2  # 避免API限流
done
```

### 指定文件夹

```bash
python3 rss-digest/scripts/upload_to_feishu.py output/digest_2026-02-17.md \
    --folder-token FolderXXXXXXXX
```

---

**提示**: 配置成功后，每次运行 `./generate_digest.sh` 都会自动上传到飞书！✨
