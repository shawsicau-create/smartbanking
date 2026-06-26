#!/bin/bash
# ============================================================================
# SmartBanking 一体化部署脚本：构建产物 + 部署 + SEO 主动推送
# ----------------------------------------------------------------------------
# 功能：
#   1. 调用 edgeone pages deploy 把 webversion/dist 部署到生产环境
#      （相比 refresh-edgeone-url.sh 的 makers deploy，pages deploy 是生产模式，
#       URL 永久稳定，搜索引擎可稳定索引，避免 3 小时过期问题）
#   2. 提取生产 URL 写入 latest-url.json / latest-url.txt 供前端 fetch
#   3. 调用百度站长平台主动推送 API，让百度小时级发现新页面
#   4. 打印一次性 SEO 提交清单（Google / Bing / 百度站长平台）
#
# 用法：
#   ./scripts/deploy-with-seo.sh
#
# 前置环境变量（写入 .env）：
#   EDGEONE_PAGES_API_TOKEN  EdgeOne Pages API Token（必需）
#   BAIDU_PUSH_TOKEN        百度站长平台「链接提交→主动推送」token（必需）
# ============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

SITE="https://smartbanking.edgeone.app"

# 加载 .env
if [[ ! -f .env ]]; then
  echo "[ERROR] .env 文件不存在: $PROJECT_ROOT/.env" >&2
  echo "提示：cp .env.example .env 后填入 EDGEONE_PAGES_API_TOKEN 与 BAIDU_PUSH_TOKEN" >&2
  exit 1
fi
# shellcheck disable=SC1091
source .env

if [[ -z "${EDGEONE_PAGES_API_TOKEN:-}" ]]; then
  echo "[ERROR] 环境变量 EDGEONE_PAGES_API_TOKEN 未设置" >&2
  exit 1
fi

if [[ -z "${BAIDU_PUSH_TOKEN:-}" ]]; then
  echo "[WARN] BAIDU_PUSH_TOKEN 未设置，将跳过百度主动推送" >&2
  echo "       获取方式: 百度搜索资源平台 → 站点管理 → 链接提交 → 主动推送 (实时)" >&2
  SKIP_BAIDU=1
else
  SKIP_BAIDU=0
fi

# 检查构建产物
if [[ ! -d webversion/dist ]]; then
  echo "[ERROR] webversion/dist 不存在，请先执行：cd webversion && pnpm build" >&2
  exit 1
fi

echo "=========================================="
echo "SmartBanking 一体化部署"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "目标: $SITE"
echo "=========================================="

# ---------------------------------------------------------------------------
# 1. 部署到 EdgeOne Pages 生产环境
# ---------------------------------------------------------------------------
echo ""
echo "[1/4] 部署 webversion/dist 到 EdgeOne Pages（生产环境）..."
DEPLOY_OUTPUT=$(cd webversion && npx edgeone pages deploy ./dist \
  -n smartbanking \
  -t "$EDGEONE_PAGES_API_TOKEN" \
  --json 2>&1) || {
    echo "[ERROR] 部署失败：" >&2
    echo "$DEPLOY_OUTPUT" >&2
    exit 1
  }
echo "✅ 部署成功"

# ---------------------------------------------------------------------------
# 2. 提取并写入最新生产 URL
# ---------------------------------------------------------------------------
echo ""
echo "[2/4] 写入最新生产 URL..."
PROD_URL=$(echo "$DEPLOY_OUTPUT" | grep -oE '"url":"[^"]+"' | head -1 | sed 's/"url":"//;s/"//g')
if [[ -z "$PROD_URL" ]]; then
  # pages deploy 输出格式可能不含 url 字段，使用 SITEMAP_BASE 兜底
  PROD_URL="$SITE"
  echo "[INFO] 部署输出未包含 url 字段，使用站点默认 URL: $PROD_URL"
else
  echo "访问 URL: $PROD_URL"
fi

REFRESHED_AT="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "$PROD_URL" > "$SCRIPT_DIR/latest_url.txt"
echo "$PROD_URL" > "$PROJECT_ROOT/webversion/public/latest-url.txt"
cat > "$PROJECT_ROOT/webversion/public/latest-url.json" <<EOF
{
  "url": "$PROD_URL",
  "refreshedAt": "$REFRESHED_AT"
}
EOF
echo "✅ 已写入:"
echo "    $SCRIPT_DIR/latest_url.txt"
echo "    webversion/public/latest-url.txt"
echo "    webversion/public/latest-url.json"

# ---------------------------------------------------------------------------
# 3. 百度主动推送（让百度小时级收录新页面）
# ---------------------------------------------------------------------------
echo ""
echo "[3/4] 百度主动推送..."
if [[ "$SKIP_BAIDU" -eq 1 ]]; then
  echo "[SKIP] 未配置 BAIDU_PUSH_TOKEN，跳过百度推送"
else
  # 一次性推送：首页 + sitemap，让百度快速建立索引入口
  BAIDU_RESP=$(curl -sS -X POST \
    "https://data.zz.baidu.com/urls?site=${SITE}&token=${BAIDU_PUSH_TOKEN}" \
    --data-urlencode "url=${PROD_URL}" \
    --data-urlencode "url=${SITE}/sitemap-index.xml" 2>&1) || {
      echo "[WARN] 百度推送失败，请检查 token / 网络" >&2
      echo "$BAIDU_RESP" >&2
    }
  echo "百度响应: $BAIDU_RESP"
fi

# ---------------------------------------------------------------------------
# 4. 输出一次性 SEO 提交清单
# ---------------------------------------------------------------------------
echo ""
echo "[4/4] 一次性 SEO 提交清单（首次部署需人工操作一次）"
echo "================================================"
echo ""
echo "🔍 Google Search Console: https://search.google.com/search-console"
echo "   - 添加资源类型: 域 (DNS TXT 验证 smartbanking.edgeone.app)"
echo "   - Sitemap 提交:  ${SITE}/sitemap-index.xml"
echo "   - URL 检查 → 请求编入索引: ${PROD_URL}"
echo ""
echo "🅱️  百度搜索资源平台: https://ziyuan.baidu.com/"
echo "   - 站点验证后 → 链接提交 → sitemap: ${SITE}/sitemap-index.xml"
echo "   - 普通收录工具: 每天可手动补提交 10 条"
echo "   - 抓取诊断: 输入 ${PROD_URL} 测试"
echo ""
echo "🅱️  Bing Webmaster Tools: https://www.bing.com/webmasters"
echo "   - Sitemap 提交: ${SITE}/sitemap-index.xml"
echo ""
echo "================================================"
echo "📋 部署后验证清单:"
echo "   1. 访问 ${SITE}/robots.txt  (应显示 Sitemap 声明)"
echo "   2. 访问 ${SITE}/sitemap-index.xml  (应能正常解析)"
echo "   3. 在百度站长平台「抓取诊断」测试首页"
echo "   4. 在 Google Search Console「URL 检查」测试首页"
echo ""
echo "✅ 完成！"