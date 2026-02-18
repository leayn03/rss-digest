#!/usr/bin/env python3
"""
尝试通过API为应用授予文件夹权限
注意：这可能需要管理员权限
"""

import requests
from dotenv import load_dotenv
import os

load_dotenv('.env')

app_id = os.getenv('FEISHU_APP_ID')
app_secret = os.getenv('FEISHU_APP_SECRET')
folder_token = os.getenv('FEISHU_FOLDER_TOKEN', 'Pz1wfydIglHWBhdFmAicScuCn6e')

print("="*60)
print("🔧 飞书文件夹权限配置工具")
print("="*60)
print()
print("注意：此工具尝试通过API配置权限")
print("如果失败，可能需要管理员在飞书后台手动配置")
print()

# 获取 token
url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
headers = {'Content-Type': 'application/json'}
data = {'app_id': app_id, 'app_secret': app_secret}

response = requests.post(url, headers=headers, json=data)
result = response.json()

if result.get('code') != 0:
    print(f"❌ 获取令牌失败: {result}")
    exit(1)

token = result.get('tenant_access_token')
print("✓ 令牌获取成功")
print()

# 方法1: 尝试获取文件夹信息
print("📝 方法1: 查询文件夹元信息...")
meta_url = f'https://open.feishu.cn/open-apis/drive/v1/metas/batch_query'
meta_headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}
meta_data = {
    'request_docs': [{
        'doc_token': folder_token,
        'doc_type': 'folder'
    }]
}

meta_response = requests.post(meta_url, headers=meta_headers, json=meta_data)
print(f"响应: {meta_response.json()}")
print()

# 方法2: 尝试获取文件夹列表（验证权限）
print("📝 方法2: 尝试列出文件夹内容...")
list_url = f'https://open.feishu.cn/open-apis/drive/v1/files?folder_token={folder_token}'
list_headers = {
    'Authorization': f'Bearer {token}'
}

list_response = requests.get(list_url, headers=list_headers)
list_result = list_response.json()
print(f"响应: {list_result}")
print()

# 建议
print("="*60)
print("💡 配置建议")
print("="*60)
print()

if list_result.get('code') == 0:
    print("✅ 应用可以访问文件夹内容")
    print()
    print("但仍然无法创建文档，这是飞书的权限限制。")
    print()
else:
    print("❌ 应用无法访问文件夹")
    print()

print("🔧 推荐解决方案:")
print()
print("方案A: 使用根目录（简单）")
print("  - 文档创建在根目录")
print("  - 手动移动到文件夹")
print("  - 已经可以使用: ./generate_digest.sh")
print()
print("方案B: 联系飞书管理员")
print("  - 让管理员在飞书管理后台")
print("  - 为应用配置「云文档」应用权限")
print("  - 特别是「在指定文件夹创建文档」权限")
print()
print("方案C: 使用服务端SDK")
print("  - 使用飞书官方SDK (larksuite-oapi)")
print("  - 可能有更多权限控制选项")
print()
