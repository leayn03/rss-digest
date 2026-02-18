#!/bin/bash
# 快速查看飞书配置状态

python3 << 'EOF'
from dotenv import load_dotenv
import os

load_dotenv('.env')

print("="*60)
print("📋 当前飞书集成配置")
print("="*60)
print()

app_id = os.getenv('FEISHU_APP_ID')
app_secret = os.getenv('FEISHU_APP_SECRET')

if not app_id or not app_secret:
    print("❌ 飞书凭证未配置")
    print()
    print("请在 .env 文件中配置:")
    print("  FEISHU_APP_ID=your_app_id")
    print("  FEISHU_APP_SECRET=your_app_secret")
    print()
    exit(1)

print(f"App ID: {app_id[:20]}...")
print(f"App Secret: {'*' * 20} (已配置 ✓)")
print()

mode = os.getenv('FEISHU_MODE', 'create')
print(f"工作模式: {mode.upper()}")
print()

if mode == 'append':
    doc_id = os.getenv('FEISHU_DOCUMENT_ID')
    if doc_id:
        print(f"✅ 追加模式 (Append Mode)")
        print(f"   - 所有报告追加到同一文档")
        print(f"   - 目标文档ID: {doc_id}")
        print(f"   - 访问链接: https://ecnjqkm7hoqs.feishu.cn/docx/{doc_id}")
    else:
        print(f"❌ 追加模式配置不完整")
        print(f"   请在 .env 中配置: FEISHU_DOCUMENT_ID")
else:
    folder = os.getenv('FEISHU_FOLDER_TOKEN')
    print(f"✅ 创建模式 (Create Mode)")
    print(f"   - 每次创建新的独立文档")
    if folder:
        print(f"   - 目标文件夹: {folder}")
        print(f"   - 文件夹链接: https://ecnjqkm7hoqs.feishu.cn/drive/folder/{folder}")
    else:
        print(f"   - 位置: 根目录（未指定文件夹）")

print()
print("="*60)
print("📖 使用方法")
print("="*60)
print()
print("生成并上传报告:")
print("  ./generate_digest.sh              # 生成昨天的报告")
print("  ./generate_digest.sh -d 2026-02-15  # 生成指定日期")
print()
print("切换模式:")
print("  编辑 .env 文件，修改 FEISHU_MODE=append 或 create")
print()
print("查看详细说明:")
print("  cat FEISHU_MODES.md")
print()
EOF
