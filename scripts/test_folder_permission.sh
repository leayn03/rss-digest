#!/bin/bash
# 测试飞书文件夹权限

python3 << 'EOF'
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv('.env')

app_id = os.getenv('FEISHU_APP_ID')
app_secret = os.getenv('FEISHU_APP_SECRET')
folder_token = os.getenv('FEISHU_FOLDER_TOKEN')

print("="*60)
print("🧪 飞书文件夹权限测试")
print("="*60)
print()

if not folder_token:
    print("❌ 未配置文件夹Token")
    print("请在 .env 中配置: FEISHU_FOLDER_TOKEN")
    exit(1)

print(f"文件夹Token: {folder_token}")
print(f"文件夹链接: https://ecnjqkm7hoqs.feishu.cn/drive/folder/{folder_token}")
print()

# 获取 token
print("📝 步骤 1: 获取访问令牌...")
url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
headers = {'Content-Type': 'application/json'}
data = {'app_id': app_id, 'app_secret': app_secret}

response = requests.post(url, headers=headers, json=data)
result = response.json()

if result.get('code') == 0:
    token = result.get('tenant_access_token')
    print("   ✅ 令牌获取成功")
else:
    print(f"   ❌ 令牌获取失败: {result}")
    exit(1)

print()
print("📝 步骤 2: 尝试在文件夹下创建测试文档...")

# 尝试创建文档
create_url = 'https://open.feishu.cn/open-apis/docx/v1/documents'
create_headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

create_data = {
    'title': '权限测试文档 - 请忽略',
    'folder_token': folder_token
}

create_response = requests.post(create_url, headers=create_headers, json=create_data)
create_result = create_response.json()

print()
print("="*60)

if create_response.status_code == 200 and create_result.get('code') == 0:
    doc_id = create_result['data']['document']['document_id']
    print("✅ 文件夹权限配置成功！")
    print("="*60)
    print()
    print(f"测试文档已创建: https://ecnjqkm7hoqs.feishu.cn/docx/{doc_id}")
    print()
    print("您可以在飞书中删除这个测试文档")
    print()
    print("🎉 现在可以正常使用了！运行:")
    print("   ./generate_digest.sh")
    print()

else:
    print("❌ 文件夹权限配置失败")
    print("="*60)
    print()
    print(f"错误码: {create_result.get('code')}")
    print(f"错误信息: {create_result.get('msg')}")

    # 详细错误说明
    error = create_result.get('error', {})
    if error:
        print()
        print("详细错误:")
        for help_info in error.get('helps', []):
            print(f"  - {help_info.get('description')}")

    print()
    print("="*60)
    print("🔧 解决方法:")
    print("="*60)
    print()

    if create_result.get('code') == 1770040:
        print("错误原因: 应用没有文件夹访问权限")
        print()
        print("请按以下步骤配置:")
        print()
        print("1. 打开文件夹:")
        print(f"   https://ecnjqkm7hoqs.feishu.cn/drive/folder/{folder_token}")
        print()
        print("2. 点击右上角「···」或「共享」按钮")
        print()
        print("3. 搜索并添加应用: RSS Digest Bot")
        print(f"   (或搜索 App ID: {app_id})")
        print()
        print("4. 授予「可编辑」权限")
        print()
        print("5. 确认添加后，重新运行此测试:")
        print("   ./test_folder_permission.sh")
        print()
    else:
        print("其他错误，请检查:")
        print("  1. 应用权限是否已开启 (docx:document, drive:drive)")
        print("  2. 权限是否已审批通过")
        print("  3. 网络连接是否正常")
        print()

    exit(1)

EOF
