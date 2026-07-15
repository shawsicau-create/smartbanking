# SmartBank Agent 阿里云部署文档

## 部署概述

SmartBank Agent 已成功部署到阿里云轻量应用服务器（SWAS），替代原有的 Cloudflare Pages 部署方案。

| 项目 | 信息 |
|------|------|
| 服务器IP | 8.137.175.215 |
| 访问地址 | http://8.137.175.215 |
| 操作系统 | CentOS 8 (x86_64) |
| 地域 | 阿里云成都 |
| 部署时间 | 2026-07-15 |

---

## 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                      用户浏览器                          │
└─────────────────────────┬───────────────────────────────┘
                          │ HTTP 80
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    Nginx 反向代理                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ 静态文件    │  │ /api/* 代理 │  │  缓存控制   │     │
│  │ (Astro SSG) │  │ → :3000     │  │             │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Express.js API Server (端口3000)            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ /api/chat   │  │ /api/debate │  │ /api/quiz   │     │
│  │ /api/generate│ │ /api/health │  │ /api/tts    │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    外部API服务                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  MiMo LLM   │  │   Tushare   │  │   高德地图   │     │
│  │  World Bank  │  │   Amap API  │  │             │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

---

## 服务器目录结构

```
/opt/smartbanking-api/          # API后端代码
├── server.js                   # Express.js 主服务
├── package.json                # 依赖配置
├── .env                        # 环境变量（API密钥）
└── node_modules/               # 依赖包

/var/www/smartbanking/static/   # 前端静态文件
├── index.html                  # 主页
├── chat/                       # 智能问答页面
├── quiz/                       # 测验页面
├── tools/                      # 工具页面
├── pbl/                        # 项目页面
├── generate/                   # 内容生成页面
├── _astro/                     # Astro构建资源
├── audio/                      # 音频文件
├── slides/                     # SVG幻灯片
└── simulations/                # 交互模拟

/etc/nginx/conf.d/
└── smartbanking.conf           # Nginx配置

/etc/systemd/system/
└── smartbank-api.service       # systemd服务配置
```

---

## 部署步骤

### 1. 服务器环境准备

```bash
# SSH登录服务器
ssh root@8.137.175.215

# 修复CentOS 8软件源（已停止维护）
sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*.repo
sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*.repo
```

### 2. 安装 Node.js 20 LTS

```bash
# 安装Node.js
yum install -y nodejs

# 验证安装
node -v    # v20.x.x
npm -v     # 10.x.x

# 安装pnpm
npm install -g pnpm
pnpm -v
```

### 3. 安装 Nginx

```bash
# 安装Nginx
yum install -y nginx

# 启动并设置开机自启
systemctl enable nginx
systemctl start nginx

# 验证
nginx -v
systemctl status nginx
```

### 4. 本地构建前端

```bash
# 在本地项目目录
cd webversion

# 安装依赖
pnpm install

# 构建静态文件
pnpm build

# 构建产物在 dist/ 目录
```

### 5. 创建 Express.js 后端

由于原项目使用 Cloudflare Pages Functions，需要创建 Express.js 版本的后端。

**server/package.json:**
```json
{
  "name": "smartbank-agent-api",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "start": "node server.js",
    "dev": "node --watch server.js"
  },
  "dependencies": {
    "express": "^4.21.0",
    "cors": "^2.8.5",
    "dotenv": "^16.4.5"
  }
}
```

**server/.env:**
```env
MIMO_API_KEY=your_mimo_api_key
TUSHARE_TOKEN=your_tushare_token
PORT=3000
```

### 6. 上传文件到服务器

```bash
# 上传静态文件
scp -r dist/* root@8.137.175.215:/var/www/smartbanking/static/

# 上传API代码
scp -r server/* root@8.137.175.215:/opt/smartbanking-api/

# 在服务器安装依赖
ssh root@8.137.175.215 "cd /opt/smartbanking-api && npm install"
```

### 7. 配置 Nginx

**/etc/nginx/conf.d/smartbanking.conf:**
```nginx
server {
    listen 80;
    server_name _;
    
    # 静态文件根目录
    root /var/www/smartbanking/static;
    index index.html;
    
    # API反向代理
    location /api/ {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 120s;
    }
    
    # Astro静态资源缓存
    location /_astro/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # 音频文件缓存
    location /audio/ {
        expires 7d;
    }
    
    # 默认路由
    location / {
        try_files $uri $uri/ $uri/index.html =404;
    }
}
```

```bash
# 测试并重载Nginx
nginx -t
nginx -s reload
```

### 8. 配置 systemd 服务

**/etc/systemd/system/smartbank-api.service:**
```ini
[Unit]
Description=SmartBank Agent API Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/smartbanking-api
ExecStart=/usr/bin/node server.js
Restart=on-failure
RestartSec=10
Environment=NODE_ENV=production
Environment=PORT=3000

[Install]
WantedBy=multi-user.target
```

```bash
# 启用并启动服务
systemctl daemon-reload
systemctl enable smartbank-api
systemctl start smartbank-api

# 验证服务状态
systemctl status smartbank-api
```

---

## 管理命令

### 服务管理

```bash
# 重启API服务
systemctl restart smartbank-api

# 停止API服务
systemctl stop smartbank-api

# 查看API服务状态
systemctl status smartbank-api

# 重启Nginx
systemctl restart nginx

# 重载Nginx配置
nginx -s reload
```

### 日志查看

```bash
# 查看API服务日志
journalctl -u smartbank-api -f

# 查看API服务最近50行日志
journalctl -u smartbank-api -n 50

# 查看Nginx访问日志
tail -f /var/log/nginx/access.log

# 查看Nginx错误日志
tail -f /var/log/nginx/error.log
```

### 测试命令

```bash
# 测试静态页面
curl -s -o /dev/null -w '%{http_code}' http://localhost

# 测试API接口
curl -s -X POST http://localhost/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"你好"}]}'

# 健康检查
curl http://localhost/api/health
```

---

## 更新部署

当需要更新代码时：

```bash
# 1. 本地构建新版本
cd webversion
pnpm build

# 2. 上传静态文件
scp -r dist/* root@8.137.175.215:/var/www/smartbanking/static/

# 3. 如有API变更，上传并重启
scp -r server/* root@8.137.175.215:/opt/smartbanking-api/
ssh root@8.137.175.215 "systemctl restart smartbank-api"
```

---

## 故障排查

### 问题1: API返回404

**原因**: Nginx代理配置错误

**解决**:
```bash
# 检查Nginx配置
cat /etc/nginx/conf.d/smartbanking.conf | grep proxy_pass

# 确保配置为（无末尾斜杠）
proxy_pass http://127.0.0.1:3000;

# 重载配置
nginx -s reload
```

### 问题2: systemd服务启动失败 (status=200/CHDIR)

**原因**: WorkingDirectory指向不存在的目录

**解决**:
```bash
# 查找node进程实际工作目录
ls -l /proc/$(pgrep -f 'node server.js')/cwd

# 更新systemd服务文件中的WorkingDirectory
vi /etc/systemd/system/smartbank-api.service

# 重新加载并重启
systemctl daemon-reload
systemctl restart smartbank-api
```

### 问题3: 端口被占用 (EADDRINUSE)

**原因**: 旧进程未完全退出

**解决**:
```bash
# 查找占用端口的进程
ss -tlnp | grep :3000

# 杀死旧进程
pkill -f 'node server.js'

# 重启服务
systemctl restart smartbank-api
```

---

## 安全建议

1. **配置防火墙**: 只开放80和443端口
2. **启用HTTPS**: 配置SSL证书（Let's Encrypt）
3. **定期更新**: 保持系统和依赖包更新
4. **备份数据**: 定期备份配置和代码
5. **监控日志**: 设置日志监控告警

---

## 与原Cloudflare部署对比

| 项目 | Cloudflare Pages | 阿里云 SWAS |
|------|------------------|-------------|
| 费用 | 免费额度有限 | 按配置付费 |
| 性能 | 全球CDN | 单区域 |
| 扩展性 | 自动扩展 | 手动扩展 |
| 控制度 | 有限 | 完全控制 |
| 后端 | Pages Functions | Express.js |
| 数据库 | D1 | 可自建 |
| 适用场景 | 小型项目 | 需要完全控制 |

---

## 联系信息

- **部署人**: 肖诗顺
- **项目**: SmartBank Agent - 金融科技实验教学智能体
- **所属**: 四川农业大学 数字经济系
