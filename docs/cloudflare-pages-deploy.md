# Cloudflare Pages 部署指南

> 适用于 smartbanking 项目（Astro + Starlight 架构）

## 前置条件

| 条件 | 说明 |
|---|---|
| Cloudflare 账号 | 已注册并可访问 [Dashboard](https://dash.cloudflare.com) |
| Node.js 20+ | `node -v` 确认 |
| pnpm | `pnpm -v` 确认 |
| wrangler | Cloudflare 官方 CLI（下方安装） |

---

## 步骤一：安装 wrangler CLI

```bash
npm install -g wrangler
wrangler --version
# 预期输出: ⛅️ wrangler 4.x.x
```

## 步骤二：登录 Cloudflare

```bash
wrangler login
```

浏览器会自动打开授权页面，点击 **Allow** 完成授权。

验证登录状态：

```bash
wrangler whoami
```

## 步骤三：创建 Cloudflare Pages 项目

在 [Cloudflare Dashboard](https://dash.cloudflare.com) 中：

1. 进入 **Workers & Pages** → **Create** → **Pages**
2. 选择 **Upload assets**（直传模式，不用 Git 集成）
3. 项目名称填 `smartbanking`
4. 点击 **Deploy** 创建空项目

## 步骤四：配置项目文件

### 4.1 根目录创建 `wrangler.toml`

在项目根目录创建：

```toml
name = "smartbanking"
compatibility_date = "2024-11-01"
pages_build_output_dir = "webversion/dist"
```

> ⚠️ **注意**：Cloudflare Pages 项目**不支持** `[build]` 配置段，否则部署时会报错：
> `Configuration file for Pages projects does not support "build"`

### 4.2 Astro 配置多平台 site URL

`webversion/astro.config.mjs`：

```javascript
// 多平台部署：GitHub Pages / Cloudflare Pages / EdgeOne
const isGitHubPages = process.env.GITHUB_PAGES === 'true';
const isCloudflarePages = process.env.CLOUDFLARE_PAGES === 'true';

const siteUrl = isGitHubPages
    ? `https://${ghOwner}.github.io`
    : isCloudflarePages
        ? 'https://smartbanking.pages.dev'
        : 'https://smartbanking.edgeone.app';

const basePath = isGitHubPages ? `/${ghRepoName}/` : '/';
```

## 步骤五：构建并部署

```bash
cd webversion

# 设置 CLOUDFLARE_PAGES 环境变量后构建
# 这样 sitemap、canonical URL 都会指向 smartbanking.pages.dev
CLOUDFLARE_PAGES=true pnpm build

# 部署到 Cloudflare Pages
wrangler pages deploy ./dist \
    --project-name=smartbanking \
    --branch=main \
    --commit-dirty=true
```

预期输出：

```
✨ Success! Uploaded 125 files (5 already uploaded) (4.33 sec)
🌎 Deploying...
✨ Deployment complete! Take a peek over at https://xxxxxxxx.smartbanking.pages.dev
```

## 步骤六：验证部署

```bash
# 检查首页
curl -sI https://smartbanking.pages.dev
# 预期: HTTP/2 200

# 检查 sitemap
curl -sI https://smartbanking.pages.dev/sitemap-index.xml
# 预期: HTTP/2 200

# 确认 sitemap 中的 URL 指向正确
curl -s https://smartbanking.pages.dev/sitemap-index.xml
# 预期: <loc>https://smartbanking.pages.dev/sitemap-0.xml</loc>
```

---

## 日常更新流程

每次更新内容后，只需执行：

```bash
cd webversion
CLOUDFLARE_PAGES=true pnpm build
wrangler pages deploy ./dist --project-name=smartbanking --branch=main --commit-dirty=true
```

---

## 常见问题

### Q: 部署报错 "does not support build"

`wrangler.toml` 中不能包含 `[build]` 段。删除该配置块即可：

```toml
# ❌ 错误 - 会导致部署失败
[build]
command = "..."

# ✅ 正确
name = "smartbanking"
compatibility_date = "2024-11-01"
pages_build_output_dir = "webversion/dist"
```

### Q: 网站返回 404

检查以下几点：
1. 构建时是否设置了 `CLOUDFLARE_PAGES=true`
2. 部署目录是否为 `./dist`（不是仓库根目录）
3. 在 Dashboard 的 Pages 项目中确认最新部署状态为 Success

### Q: Git 集成部署后网站白屏

Cloudflare Pages 的 Git 集成**不读取** `wrangler.toml`。若使用 Git 集成，必须在 Dashboard 中手动配置：

| 配置项 | 值 |
|---|---|
| Framework preset | `Astro` |
| Build command | `cd webversion && pnpm install --frozen-lockfile && pnpm build` |
| Build output directory | `webversion/dist` |
