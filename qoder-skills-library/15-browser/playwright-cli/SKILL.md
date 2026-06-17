---
name: playwright-cli
description: Playwright CLI Skill
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
  - testing

---

# Playwright CLI Skill

浏览器自动化命令行工具，用于网页截图、PDF生成、代码录制、浏览器操作等。

## 安装

```bash
npm install -g @playwright/cli
```

## 常用命令

### 截图
```bash
# 网页截图
playwright screenshot https://example.com output.png

# 指定视口大小
playwright screenshot --viewport-size=1280,720 https://example.com output.png

# 完整页面截图
playwright screenshot --full-page https://example.com output.png
```

### 生成 PDF
```bash
playwright pdf https://example.com output.pdf
```

### 打开浏览器
```bash
# 打开 Chromium
playwright cr https://kns.cnki.net/

# 打开 Firefox
playwright ff https://example.com

# 打开 WebKit
playwright wk https://example.com
```

### 代码生成（录制操作）
```bash
# 录制操作并生成代码
playwright codegen https://example.com

# 录制为 Python 脚本
playwright codegen --target=python https://example.com
```

### 安装浏览器
```bash
# 安装所有浏览器
playwright install

# 仅安装 Chromium
playwright install chromium

# 安装浏览器依赖（Linux）
playwright install-deps
```

## 使用示例

### 知网检索自动化
```bash
# 1. 打开知网
playwright cr https://kns.cnki.net/

# 2. 录制操作生成脚本
playwright codegen --target=python https://kns.cnki.net/
```

### 批量截图
```bash
# 截图保存为文件
playwright screenshot --viewport-size=1920,1080 https://lib.sicau.edu.cn lib.png
```

### 保存网页为PDF
```bash
# 将文献页面保存为PDF
playwright pdf https://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=... paper.pdf
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--viewport-size=W,H` | 设置视口大小 |
| `--full-page` | 完整页面截图 |
| `--browser=BROWSER` | 指定浏览器 (chromium/firefox/webkit) |
| `--target=LANG` | 代码生成目标语言 (python/javascript) |
| `--headless` | 无头模式 |
| `--timeout=MS` | 超时时间 |

## 注意事项

1. 首次使用需安装浏览器：`playwright install chromium`
2. 部分网站需要登录，建议先用 `playwright codegen` 录制登录流程
3. 机构内网资源需要连接VPN或校园网
