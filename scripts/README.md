# EdgeOne Pages URL 自动刷新指南

## 问题背景

EdgeOne Pages 在「全球可用区（含中国大陆）」区域部署时，**默认域名** 强制要求使用 **3 小时有效期的预览链接**（URL 带 `eo_token` 参数）。过期后返回 401。

## 解决方案

自动化脚本 `refresh-edgeone-url.sh` 会：
1. 重新执行 `edgeone makers deploy` → 触发平台生成新的 3 小时 token
2. 把新链接写入：
   - `scripts/latest_url.txt`（本地文件）
   - `webversion/public/latest-url.json`（部署后可访问）
3. 输出到终端和日志

## 安装定时任务（macOS launchd）

```bash
# 1. 复制 plist 到 LaunchAgents 目录
cp scripts/com.smartbanking.refresh-edgeone-url.plist ~/Library/LaunchAgents/

# 2. 加载任务（立即执行 + 每 2 小时重复）
launchctl load ~/Library/LaunchAgents/com.smartbanking.refresh-edgeone-url.plist

# 3. 查看状态
launchctl list | grep smartbanking

# 4. 立即手动触发一次（不等定时）
launchctl start com.smartbanking.refresh-edgeone-url

# 5. 查看日志
tail -f scripts/refresh.log
```

## 停止定时任务

```bash
# 卸载任务
launchctl unload ~/Library/LaunchAgents/com.smartbanking.refresh-edgeone-url.plist
```

## 手动执行

```bash
./scripts/refresh-edgeone-url.sh
```

输出示例：

```
==========================================
EdgeOne Pages 自动刷新 - 2026-06-26 22:00:00
==========================================
✅ 部署成功
新预览链接: https://smartbanking-vbxpnwfs.edgeone.run?eo_token=xxx&eo_time=xxx
有效期至:  2026-06-27 01:00:00

已写入：
  - scripts/latest_url.txt
  - webversion/public/latest-url.txt
  - webversion/public/latest-url.json
```

## 架构图

```
┌─────────────────────────────────────┐
│ launchd 每 2 小时触发               │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│ refresh-edgeone-url.sh              │
│  - source .env                      │
│  - npx edgeone makers deploy        │
│  - 提取 eo_token URL                │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│ 输出：                              │
│  - latest_url.txt                   │
│  - public/latest-url.json           │
└─────────────────────────────────────┘
```

## 后续优化（未实现）

- [ ] 通过 webhook 推送新链接到企业微信 / 钉钉群
- [ ] 写入 README.md 文件 + git push → 触发 CI/CD 自动重新部署（自更新循环）
- [ ] 接入监控告警（链接失效时通知）
