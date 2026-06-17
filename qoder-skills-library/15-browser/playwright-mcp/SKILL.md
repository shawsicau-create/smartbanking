---
name: playwright-mcp
description: Playwright MCP Skill
workflow_stage: communication
compatibility:
  - claude-code
  - cursor
  - codex
author: Qoder Skills Library
version: 1.0.0
tags:
  - browser
  - playwright
  - mcp

---

# Playwright MCP Skill

浏览器自动化 MCP 工具，基于 Playwright 实现网页浏览、点击、表单填写、截图等功能。

## 安装

已全局安装：
```bash
npm install -g @playwright/mcp
```

## 启动 MCP Server

```bash
npx @playwright/mcp
```

可选参数：
- `--allowed-hosts '*'`: 允许所有域名
- `--allowed-origins '*'`: 允许所有来源
- `--viewport-size 1280,720`: 设置视口大小

## 使用方式

通过 MCP 客户端调用以下工具：

### 浏览器操作

| 工具 | 功能 |
|------|------|
| `browser_navigate` | 导航到URL |
| `browser_click` | 点击元素 |
| `browser_fill` | 填写表单 |
| `browser_select` | 选择下拉框 |
| `browser_hover` | 悬停元素 |
| `browser_press` | 按键操作 |
| `browser_screenshot` | 截图 |
| `browser_close` | 关闭浏览器 |

### 示例

```javascript
// 导航到知网
await browser_navigate({ url: "https://kns.cnki.net/" });

// 填写搜索框
await browser_fill({ selector: "#SearchWord", value: "金融治理" });

// 点击搜索按钮
await browser_click({ selector: "#SearchBtn" });

// 截图保存
await browser_screenshot({ path: "search_result.png" });
```

## 适用场景

- 自动化登录知网、万方等数据库
- 批量检索和下载文献
- 网页数据采集
- 自动化测试

## 注意事项

1. 需要安装 Playwright 浏览器：`npx playwright install chromium`
2. 部分网站有反爬虫机制，需控制访问频率
3. 机构账号登录时注意IP限制
