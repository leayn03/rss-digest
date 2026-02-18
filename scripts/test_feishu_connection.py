#!/usr/bin/env python3
"""
Test Feishu API connection and credentials.

这个脚本用于测试飞书API连接和凭证是否配置正确。

Usage:
    python scripts/test_feishu_connection.py
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_feishu_connection():
    """Test Feishu API connection."""
    print("=" * 60)
    print("🧪 飞书API连接测试")
    print("=" * 60)
    print()

    # Get credentials
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")

    if not app_id or not app_secret:
        print("❌ 错误: 未找到飞书凭证")
        print()
        print("请确保:")
        print("  1. 已创建 .env 文件")
        print("  2. 已填写 FEISHU_APP_ID 和 FEISHU_APP_SECRET")
        print()
        print("示例 .env 文件:")
        print("  FEISHU_APP_ID=cli_xxxxxxxxxxxx")
        print("  FEISHU_APP_SECRET=your_secret_here")
        sys.exit(1)

    print(f"✓ App ID: {app_id[:15]}...")
    print(f"✓ App Secret: {'*' * 10} (已隐藏)")
    print()

    # Test 1: Get tenant access token
    print("📝 测试 1: 获取访问令牌")
    print("-" * 60)

    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    data = {
        "app_id": app_id,
        "app_secret": app_secret
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()

        if result.get("code") == 0:
            token = result.get("tenant_access_token")
            print(f"✅ 成功获取访问令牌")
            print(f"   令牌: {token[:20]}...")
            print(f"   过期时间: {result.get('expire', 'N/A')} 秒")
            print()
            return True, token
        else:
            error_msg = result.get('msg', 'Unknown error')
            error_code = result.get('code', 'N/A')
            print(f"❌ 获取令牌失败: [{error_code}] {error_msg}")
            print()
            print("可能的原因:")
            print("  1. App ID 或 App Secret 不正确")
            print("  2. 应用未启用或已被禁用")
            print("  3. 网络连接问题")
            return False, None

    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        print("   请检查网络连接")
        return False, None
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误: {e}")
        return False, None
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False, None


def test_create_document(token: str):
    """Test creating a document."""
    print("📝 测试 2: 创建测试文档")
    print("-" * 60)

    url = "https://open.feishu.cn/open-apis/docx/v1/documents"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "title": "🧪 RSS Digest - 连接测试文档"
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()

        if result.get("code") == 0:
            doc_id = result.get("data", {}).get("document", {}).get("document_id")
            doc_url = f"https://bytedance.feishu.cn/docx/{doc_id}"

            print(f"✅ 成功创建测试文档")
            print(f"   文档ID: {doc_id}")
            print(f"   访问链接: {doc_url}")
            print()
            print("💡 提示: 请访问上述链接验证文档是否创建成功")
            print("   如果链接无法访问，请将域名替换为你的飞书租户域名")
            print()
            return True, doc_id
        else:
            error_msg = result.get('msg', 'Unknown error')
            error_code = result.get('code', 'N/A')
            print(f"❌ 创建文档失败: [{error_code}] {error_msg}")
            print()

            if error_code == 99991668:
                print("权限不足！")
                print("请确保应用已开启以下权限:")
                print("  • docx:document - 创建、编辑、删除文档")
                print("  • drive:drive - 访问云空间")
                print()
                print("配置步骤:")
                print("  1. 访问 https://open.feishu.cn/app/")
                print("  2. 选择你的应用")
                print("  3. 进入「权限管理」")
                print("  4. 搜索并开启上述权限")
                print("  5. 等待管理员审批（如需要）")
            return False, None

    except Exception as e:
        print(f"❌ 错误: {e}")
        return False, None


def main():
    """Run all tests."""
    # Test 1: Get access token
    success, token = test_feishu_connection()
    if not success:
        print("=" * 60)
        print("❌ 测试失败")
        print("=" * 60)
        sys.exit(1)

    # Test 2: Create document
    success, doc_id = test_create_document(token)

    print("=" * 60)
    if success:
        print("✅ 所有测试通过！")
        print()
        print("你的飞书集成配置正确，可以开始使用了！")
        print()
        print("下一步:")
        print("  1. 运行 ./generate_digest.sh 生成报告")
        print("  2. 报告会自动上传到飞书文档")
        print("  3. 访问飞书云空间查看你的报告")
    else:
        print("❌ 测试失败")
        print()
        print("请根据上述错误信息排查问题，或查看:")
        print("  • FEISHU_INTEGRATION.md - 详细配置指南")
        print("  • https://open.feishu.cn/document/ - 飞书开放平台文档")
    print("=" * 60)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
