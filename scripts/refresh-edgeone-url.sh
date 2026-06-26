#!/bin/bash
# ============================================================================
# EdgeOne Pages 自动刷新脚本
# ----------------------------------------------------------------------------
# 功能：重新部署 EdgeOne Pages 项目，生成新的 3 小时有效预览链接
# 用途：解决"全球可用区（含中国大陆）"区域的 3 小时 token 过期问题
# 用法：
#   1. 手动执行：./scripts/refresh-edgeone-url.sh
#   2. 定时执行：配合 macOS launchd 每 2 小时自动执行一次
# 输出：
#   - 控制台打印最新预览链接
#   - 写入 scripts/latest_url.txt
#   - 写入 webversion/public/latest-url.json（部署后可访问）
# ============================================================================

set -euo pipefail

# launchd / cron 等后台运行环境不加载用户 shell 的 PATH，需显式设置
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

# 切换到项目根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# 加载 .env（EdgeOne API Token）
if [[ ! -f .env ]]; then
  echo "[ERROR] .env 文件不存在: $PROJECT_ROOT/.env" >&2
  exit 1
fi

# shellcheck disable=SC1091
source .env

if [[ -z "${EDGEONE_PAGES_API_TOKEN:-}" ]]; then
  echo "[ERROR] 环境变量 EDGEONE_PAGES_API_TOKEN 未设置" >&2
  exit 1
fi

# 检查 dist 是否存在
if [[ ! -d webversion/dist ]]; then
  echo "[ERROR] webversion/dist 不存在，请先执行：cd webversion && pnpm build" >&2
  exit 1
fi

echo "=========================================="
echo "EdgeOne Pages 自动刷新 - $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

# 执行部署
DEPLOY_OUTPUT=$(cd webversion && npx edgeone makers deploy ./dist \
  -n smartbanking \
  -t "$EDGEONE_PAGES_API_TOKEN" \
  --json 2>&1) || {
  echo "[ERROR] 部署失败：" >&2
  echo "$DEPLOY_OUTPUT" >&2
  exit 1
}

# 提取 JSON 中的 url 字段（--json 输出为单行 JSON）
NEW_URL=$(echo "$DEPLOY_OUTPUT" | grep -oE '"url":"[^"]+"' | head -1 | sed 's/"url":"//;s/"//g')

if [[ -z "$NEW_URL" ]]; then
  echo "[ERROR] 未能从部署输出中提取 URL：" >&2
  echo "$DEPLOY_OUTPUT" >&2
  exit 1
fi

EXPIRE_TIME=$(date -v+3H '+%Y-%m-%d %H:%M:%S' 2>/dev/null \
  || date -d '+3 hours' '+%Y-%m-%d %H:%M:%S')

echo ""
echo "✅ 部署成功"
echo "新预览链接: $NEW_URL"
echo "有效期至:  $EXPIRE_TIME"
echo ""

# 1. 写入本地文件
echo "$NEW_URL" > "$SCRIPT_DIR/latest_url.txt"
echo "$NEW_URL" > "$PROJECT_ROOT/webversion/public/latest-url.txt"
echo "$EXPIRE_TIME" > "$SCRIPT_DIR/latest_url_expire.txt"

# 2. 写入 JSON（供前端 fetch）
cat > "$PROJECT_ROOT/webversion/public/latest-url.json" <<EOF
{
  "url": "$NEW_URL",
  "expireAt": "$EXPIRE_TIME",
  "refreshedAt": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
}
EOF

echo "已写入："
echo "  - $SCRIPT_DIR/latest_url.txt"
echo "  - webversion/public/latest-url.txt"
echo "  - webversion/public/latest-url.json"
echo ""
echo "✅ 完成。复制上面的链接在浏览器打开即可访问。"
