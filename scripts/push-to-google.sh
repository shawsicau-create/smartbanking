#!/bin/bash
# ============================================================================
# Google Indexing API 主动推送脚本
# ----------------------------------------------------------------------------
# 前置条件：
#   1. 创建 Google Cloud 项目并启用 Indexing API
#   2. 创建 Service Account 并下载 JSON 密钥
#   3. 在 Search Console 中添加 Service Account 为验证用户
#   4. 安装 gcloud CLI 或使用 curl 直接调用
#
# 环境变量：
#   GOOGLE_SERVICE_ACCOUNT_KEY  Service Account JSON 密钥文件路径
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SITE_URL="https://shawsicau-create.github.io/smartbanking"

# 获取 sitemap 中的所有 URL
SITEMAP_URL="${SITE_URL}/sitemap-index.xml"

echo "=========================================="
echo "Google Indexing API 主动推送"
echo "目标站点: ${SITE_URL}"
echo "=========================================="

# 检查依赖
if ! command -v curl &> /dev/null; then
    echo "[ERROR] 需要安装 curl" >&2
    exit 1
fi

# 提示用户配置
echo ""
echo "请确保已完成以下配置："
echo "1. 创建 Google Cloud 项目"
echo "2. 启用 Indexing API"
echo "3. 创建 Service Account"
echo "4. 在 Search Console 添加 Service Account 邮箱为验证用户"
echo ""
echo "Google Search Console: https://search.google.com/search-console"
echo "Google Cloud Console: https://console.cloud.google.com/"
echo ""

# 获取访问令牌（需要 gcloud CLI）
if command -v gcloud &> /dev/null; then
    echo "正在获取访问令牌..."
    ACCESS_TOKEN=$(gcloud auth print-access-token)
    
    # 推送首页
    echo "推送首页..."
    curl -s -X POST \
        "https://indexing.googleapis.com/v3/urlNotifications:publish" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}" \
        -d "{\"url\": \"${SITE_URL}/\", \"type\": \"URL_UPDATED\"}"
    echo ""
    
    echo "✅ 首页推送完成"
else
    echo "[WARN] 未安装 gcloud CLI，无法自动推送"
    echo "请手动在 Google Search Console 的 URL 检查工具中请求索引"
fi

echo ""
echo "=========================================="
echo "手动操作建议："
echo "1. 访问 Google Search Console"
echo "2. 使用 URL 检查工具逐页请求索引"
echo "3. 重点页面："
echo "   - 首页: ${SITE_URL}/"
echo "   - 绪论: ${SITE_URL}/ch01/"
echo "   - 环境搭建: ${SITE_URL}/ch02/"
echo "=========================================="
