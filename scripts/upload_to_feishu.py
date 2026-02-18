#!/usr/bin/env python3
"""
Upload markdown report to Feishu (Lark) document.

This script uploads the generated markdown report to a specified Feishu folder.
It requires Feishu API credentials (App ID and App Secret) to be configured.

Usage:
    python scripts/upload_to_feishu.py <markdown_file_path> [--folder-token FOLDER_TOKEN]

Environment variables (or .env file):
    FEISHU_APP_ID: Your Feishu app ID
    FEISHU_APP_SECRET: Your Feishu app secret
    FEISHU_FOLDER_TOKEN: Default folder token (optional, can be overridden by --folder-token)

Requirements:
    pip install requests python-dotenv
"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class FeishuDocumentUploader:
    """Upload markdown content to Feishu document."""

    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
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

    def convert_markdown_to_blocks(self, markdown_content: str) -> list:
        """
        Convert markdown content to Feishu document blocks.

        This is a simple converter. For more complex markdown,
        consider using a markdown parser library.
        """
        blocks = []
        lines = markdown_content.split('\n')

        current_block = []
        in_code_block = False
        code_language = ""

        for line in lines:
            # Handle code blocks
            if line.strip().startswith('```'):
                if in_code_block:
                    # End of code block
                    blocks.append({
                        "block_type": 1,  # Text block
                        "text": {
                            "elements": [{
                                "text_run": {
                                    "text": '\n'.join(current_block),
                                    "style": {}
                                }
                            }],
                            "style": {}
                        }
                    })
                    current_block = []
                    in_code_block = False
                else:
                    # Start of code block
                    if current_block:
                        blocks.append({
                            "block_type": 1,
                            "text": {
                                "elements": [{
                                    "text_run": {
                                        "text": '\n'.join(current_block),
                                        "style": {}
                                    }
                                }],
                                "style": {}
                            }
                        })
                        current_block = []
                    code_language = line.strip()[3:].strip()
                    in_code_block = True
                continue

            if in_code_block:
                current_block.append(line)
            else:
                current_block.append(line)

                # Create block on empty line (paragraph separator)
                if not line.strip() and current_block[:-1]:
                    blocks.append({
                        "block_type": 1,
                        "text": {
                            "elements": [{
                                "text_run": {
                                    "text": '\n'.join(current_block[:-1]),
                                    "style": {}
                                }
                            }],
                            "style": {}
                        }
                    })
                    current_block = []

        # Add remaining content
        if current_block:
            blocks.append({
                "block_type": 1,
                "text": {
                    "elements": [{
                        "text_run": {
                            "text": '\n'.join(current_block),
                            "style": {}
                        }
                    }],
                    "style": {}
                }
            })

        return blocks

    def create_document(self, title: str, folder_token: str = None) -> str:
        """
        Create a new Feishu document and return its token.

        每次调用都会创建一个全新的文档，不会覆盖已有文档。

        Args:
            title: 文档标题
            folder_token: 可选，文件夹token，不指定则创建在根目录

        Returns:
            document_id: 新创建的文档ID
        """
        if not self.tenant_access_token:
            self.get_tenant_access_token()

        url = "https://open.feishu.cn/open-apis/docx/v1/documents"
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": "application/json"
        }

        # 根据飞书API文档构建请求
        data = {
            "title": title
        }

        # 如果指定了文件夹，将文档创建在该文件夹下
        if folder_token:
            data["folder_token"] = folder_token

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()

            if result.get("code") == 0:
                doc_token = result.get("data", {}).get("document", {}).get("document_id")
                print(f"✓ 成功创建新文档: {title}")
                print(f"  文档ID: {doc_token}")
                return doc_token
            else:
                error_msg = result.get('msg', 'Unknown error')
                error_code = result.get('code', 'N/A')
                raise Exception(f"Failed to create document: [{error_code}] {error_msg}")
        except Exception as e:
            raise Exception(f"Error creating Feishu document: {e}")

    def get_document_blocks(self, doc_token: str) -> dict:
        """
        获取文档的所有块，主要是为了获取根块ID。

        Args:
            doc_token: 文档ID

        Returns:
            包含block信息的字典
        """
        if not self.tenant_access_token:
            self.get_tenant_access_token()

        url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{doc_token}"
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()

            if result.get("code") == 0:
                return result.get("data", {}).get("block", {})
            else:
                raise Exception(f"Failed to get document blocks: {result.get('msg')}")
        except Exception as e:
            raise Exception(f"Error getting document blocks: {e}")

    def write_content_to_document(self, doc_token: str, content: str) -> bool:
        """
        Write markdown content to Feishu document.

        将markdown内容写入飞书文档。会先获取文档的根块ID，
        然后将内容追加到文档中。

        Args:
            doc_token: 文档ID
            content: markdown内容

        Returns:
            True if successful
        """
        if not self.tenant_access_token:
            self.get_tenant_access_token()

        # 获取文档根块信息
        print("  获取文档块信息...")
        root_block = self.get_document_blocks(doc_token)
        # 文档ID本身就是根块ID
        parent_block_id = doc_token

        # 构建批量创建块的API URL
        url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{parent_block_id}/children"
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": "application/json"
        }

        # 分块处理内容（飞书API有长度限制）
        max_length = 4000  # 保守一些，避免超过限制
        content_chunks = []

        # 将内容按段落分割，避免在段落中间截断
        paragraphs = content.split('\n\n')
        current_chunk = []
        current_length = 0

        for para in paragraphs:
            para_length = len(para)
            if current_length + para_length > max_length and current_chunk:
                # 当前块已满，保存并开始新块
                content_chunks.append('\n\n'.join(current_chunk))
                current_chunk = [para]
                current_length = para_length
            else:
                current_chunk.append(para)
                current_length += para_length + 2  # +2 for '\n\n'

        if current_chunk:
            content_chunks.append('\n\n'.join(current_chunk))

        # 批量创建文本块
        print(f"  写入内容（共 {len(content_chunks)} 个块）...")
        for i, chunk in enumerate(content_chunks, 1):
            # 构建块数据
            children = [{
                "block_type": 1,  # 文本块
                "text": {
                    "elements": [{
                        "text_run": {
                            "text": chunk
                        }
                    }],
                    "style": {}
                }
            }]

            data = {
                "children": children,
                "index": -1  # -1 表示追加到末尾
            }

            try:
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                result = response.json()

                if result.get("code") != 0:
                    error_msg = result.get('msg', 'Unknown error')
                    error_code = result.get('code', 'N/A')
                    raise Exception(f"Failed to write content: [{error_code}] {error_msg}")

                print(f"    ✓ 块 {i}/{len(content_chunks)} 写入成功")

            except Exception as e:
                raise Exception(f"Error writing block {i} to Feishu document: {e}")

        return True

    def upload_markdown_file(self, file_path: str, folder_token: str = None) -> str:
        """
        Upload markdown file to Feishu document.

        每次调用都会创建一个全新的文档，不会覆盖已有文档。

        Args:
            file_path: Path to markdown file
            folder_token: Feishu folder token (optional)

        Returns:
            Document URL (https://your-domain.feishu.cn/docx/{doc_token})
        """
        # Read markdown file
        print(f"\n📖 读取文件: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            file_size = len(content)
            print(f"  文件大小: {file_size:,} 字符")
        except Exception as e:
            raise Exception(f"Error reading markdown file: {e}")

        # Extract title from filename
        filename = Path(file_path).stem
        # 提取日期并格式化标题
        title = f"RSS每日报告 - {filename.replace('digest_', '')}"

        # Create document
        print(f"\n📝 创建飞书文档...")
        doc_token = self.create_document(title, folder_token)

        # Write content
        print(f"\n✍️  写入内容到文档...")
        self.write_content_to_document(doc_token, content)
        print(f"\n✓ 内容写入完成！")

        # Generate document URL
        # 注意：实际的域名可能是 xxx.feishu.cn 或 xxx.larksuite.com
        # 这里使用通用格式，用户需要根据自己的租户替换域名
        doc_url = f"https://bytedance.feishu.cn/docx/{doc_token}"

        print(f"\n📄 文档创建成功！")
        print(f"  标题: {title}")
        print(f"  文档ID: {doc_token}")
        print(f"  访问链接: {doc_url}")
        print(f"\n💡 提示: 如果链接无法访问，请将域名 'bytedance.feishu.cn' 替换为你的飞书租户域名")

        return doc_url


def main():
    parser = argparse.ArgumentParser(
        description="Upload markdown report to Feishu document"
    )
    parser.add_argument(
        "markdown_file",
        help="Path to markdown file"
    )
    parser.add_argument(
        "--folder-token",
        help="Feishu folder token (optional, uses FEISHU_FOLDER_TOKEN env var if not specified)"
    )
    parser.add_argument(
        "--app-id",
        help="Feishu app ID (optional, uses FEISHU_APP_ID env var if not specified)"
    )
    parser.add_argument(
        "--app-secret",
        help="Feishu app secret (optional, uses FEISHU_APP_SECRET env var if not specified)"
    )

    args = parser.parse_args()

    # Get credentials
    app_id = args.app_id or os.getenv("FEISHU_APP_ID")
    app_secret = args.app_secret or os.getenv("FEISHU_APP_SECRET")
    folder_token = args.folder_token or os.getenv("FEISHU_FOLDER_TOKEN")

    if not app_id or not app_secret:
        print("Error: Feishu credentials not provided.")
        print("Please set FEISHU_APP_ID and FEISHU_APP_SECRET environment variables,")
        print("or provide them via --app-id and --app-secret arguments.")
        sys.exit(1)

    # Check if file exists
    if not os.path.exists(args.markdown_file):
        print(f"Error: File not found: {args.markdown_file}")
        sys.exit(1)

    try:
        print("=" * 60)
        print("🚀 飞书文档上传工具")
        print("=" * 60)

        # Upload to Feishu
        uploader = FeishuDocumentUploader(app_id, app_secret)
        doc_url = uploader.upload_markdown_file(args.markdown_file, folder_token)

        # Save URL to a file for reference
        url_file = args.markdown_file.replace('.md', '_feishu_url.txt')
        with open(url_file, 'w', encoding='utf-8') as f:
            f.write(doc_url)

        print(f"\n💾 URL已保存到: {url_file}")
        print("\n" + "=" * 60)
        print("✅ 上传完成！")
        print("=" * 60)

    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ 上传失败")
        print("=" * 60)
        print(f"\n错误信息: {e}")
        print("\n请检查:")
        print("  1. 飞书App ID和Secret是否正确")
        print("  2. 应用权限是否已配置（docx:document, drive:drive）")
        print("  3. 网络连接是否正常")
        print("  4. markdown文件是否存在")
        sys.exit(1)


if __name__ == "__main__":
    main()
