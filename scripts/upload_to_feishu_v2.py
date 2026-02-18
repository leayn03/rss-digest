#!/usr/bin/env python3
"""
Upload markdown report to Feishu (Lark) document - Version 2
支持两种模式：
1. append - 追加到现有文档
2. create - 创建新文档

Usage:
    python scripts/upload_to_feishu_v2.py <markdown_file_path>

Environment variables (from .env file):
    FEISHU_APP_ID: Your Feishu app ID
    FEISHU_APP_SECRET: Your Feishu app secret
    FEISHU_MODE: 'append' or 'create' (default: create)
    FEISHU_DOCUMENT_ID: Target document ID for append mode
    FEISHU_FOLDER_TOKEN: Folder token for create mode
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FeishuUploader:
    """Upload content to Feishu document."""

    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.tenant_access_token = None

    def get_tenant_access_token(self) -> str:
        """Get tenant access token from Feishu API."""
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()

            if result.get("code") == 0:
                self.tenant_access_token = result.get("tenant_access_token")
                return self.tenant_access_token
            else:
                raise Exception(f"Failed to get access token: {result.get('msg')}")
        except Exception as e:
            raise Exception(f"Error getting Feishu access token: {e}")

    def create_document(self, title: str, folder_token: str = None) -> str:
        """Create a new Feishu document."""
        if not self.tenant_access_token:
            self.get_tenant_access_token()

        url = "https://open.feishu.cn/open-apis/docx/v1/documents"
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": "application/json"
        }

        data = {"title": title}
        if folder_token:
            data["folder_token"] = folder_token

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()

            if result.get("code") == 0:
                doc_id = result.get("data", {}).get("document", {}).get("document_id")
                return doc_id
            else:
                raise Exception(f"Failed to create document: {result.get('msg')}")
        except Exception as e:
            raise Exception(f"Error creating document: {e}")

    def append_content(self, doc_id: str, content: str, add_separator: bool = True):
        """Append content to existing document."""
        if not self.tenant_access_token:
            self.get_tenant_access_token()

        # 添加分隔符
        if add_separator:
            separator = "\n\n" + "="*60 + "\n\n"
            content = separator + content

        # 分块上传（每块最多3000字符）
        chunk_size = 3000
        chunks = []
        for i in range(0, len(content), chunk_size):
            chunks.append(content[i:i+chunk_size])

        url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children"
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": "application/json"
        }

        print(f"📝 开始追加内容（共 {len(content)} 字符，分 {len(chunks)} 块）...")

        for idx, chunk in enumerate(chunks, 1):
            data = {
                "children": [{
                    "block_type": 2,  # 文本块
                    "text": {
                        "elements": [{
                            "text_run": {
                                "content": chunk
                            }
                        }]
                    }
                }],
                "index": -1  # 追加到末尾
            }

            try:
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                result = response.json()

                if result.get("code") != 0:
                    raise Exception(f"Failed to append content: {result.get('msg')}")

                print(f"   ✓ 块 {idx}/{len(chunks)} 追加成功")
            except Exception as e:
                raise Exception(f"Error appending block {idx}: {e}")

        return True

    def upload_to_new_document(self, file_path: str, folder_token: str = None) -> str:
        """Create new document and upload content."""
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract date from filename
        filename = Path(file_path).stem
        date_str = filename.replace('digest_', '')
        title = f"RSS Digest - {date_str}"

        # Create document
        print(f"📝 创建新文档: {title}")
        doc_id = self.create_document(title, folder_token)
        print(f"   ✓ 文档创建成功: {doc_id}")

        # Upload content
        self.append_content(doc_id, content, add_separator=False)

        return doc_id

    def upload_to_existing_document(self, file_path: str, doc_id: str) -> str:
        """Append content to existing document."""
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract date from filename
        filename = Path(file_path).stem
        date_str = filename.replace('digest_', '')

        # Add header with date
        header = f"\n\n# RSS Digest - {date_str}\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        full_content = header + content

        # Append to document
        print(f"📝 追加到文档: {doc_id}")
        self.append_content(doc_id, full_content, add_separator=True)

        return doc_id


def main():
    """Main function."""
    print("="*60)
    print("🚀 飞书文档上传工具 v2")
    print("="*60)

    # Check arguments
    if len(sys.argv) < 2:
        print("\n❌ 错误: 缺少文件路径参数")
        print("\n用法:")
        print("  python scripts/upload_to_feishu_v2.py <markdown_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Check file exists
    if not os.path.exists(file_path):
        print(f"\n❌ 错误: 文件不存在: {file_path}")
        sys.exit(1)

    # Load configuration
    app_id = os.getenv('FEISHU_APP_ID')
    app_secret = os.getenv('FEISHU_APP_SECRET')
    mode = os.getenv('FEISHU_MODE', 'create').lower()
    doc_id = os.getenv('FEISHU_DOCUMENT_ID')
    folder_token = os.getenv('FEISHU_FOLDER_TOKEN')

    # Validate credentials
    if not app_id or not app_secret:
        print("\n❌ 错误: 未配置飞书应用凭证")
        print("请在 .env 文件中配置 FEISHU_APP_ID 和 FEISHU_APP_SECRET")
        sys.exit(1)

    print(f"\n📖 读取文件: {file_path}")
    file_size = os.path.getsize(file_path)
    print(f"   文件大小: {file_size:,} 字节")

    print(f"\n⚙️  工作模式: {mode}")

    try:
        uploader = FeishuUploader(app_id, app_secret)

        if mode == 'append':
            # 追加模式
            if not doc_id:
                print("\n❌ 错误: 追加模式需要配置 FEISHU_DOCUMENT_ID")
                sys.exit(1)

            print(f"   目标文档: {doc_id}")
            uploader.upload_to_existing_document(file_path, doc_id)
            doc_url = f"https://ecnjqkm7hoqs.feishu.cn/docx/{doc_id}"

            print("\n" + "="*60)
            print("✅ 追加成功！")
            print("="*60)
            print(f"\n📄 访问文档: {doc_url}")

        else:
            # 创建模式
            if folder_token:
                print(f"   目标文件夹: {folder_token}")
            else:
                print(f"   位置: 根目录")

            new_doc_id = uploader.upload_to_new_document(file_path, folder_token)
            doc_url = f"https://ecnjqkm7hoqs.feishu.cn/docx/{new_doc_id}"

            print("\n" + "="*60)
            print("✅ 上传成功！")
            print("="*60)
            print(f"\n📄 访问文档: {doc_url}")

            # Save URL to file
            url_file = file_path.replace('.md', '_feishu_url.txt')
            with open(url_file, 'w') as f:
                f.write(f"{doc_url}\n")
            print(f"✓ URL已保存: {url_file}")

    except Exception as e:
        print("\n" + "="*60)
        print("❌ 上传失败")
        print("="*60)
        print(f"\n错误信息: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
