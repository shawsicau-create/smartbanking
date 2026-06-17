---
name: imap-smtp-email
description: Send and receive emails via IMAP/SMTP protocols for automated research communication and notification workflows.
workflow_stage: communication
compatibility:
  - claude-code
  - cursor
  - codex
author: Qoder Skills Library
version: 1.0.0
tags:
  - messaging
  - email
  - IMAP
  - SMTP
---

# Imap Smtp Email

## Purpose

通过IMAP/SMTP协议收发电子邮件，支持自动化研究通讯和通知工作流。适用于研究协作、投稿通知和学术沟通自动化。

## When to Use

- 需要自动化邮件收发时使用
- 研究通讯和通知工作流时触发
- 触发词："发邮件"、"收邮件"、"email"、"SMTP"

## Instructions

### Step 1
确认邮件操作：发送/接收/搜索/附件处理
### Step 2
配置IMAP/SMTP连接参数
### Step 3
构建邮件内容(支持模板)
### Step 4
执行邮件操作并验证结果
### Step 5
生成操作摘要和状态报告

## Example Prompts

- "发送论文提交通知邮件"
- "搜索收件箱中的审稿意见"
- "自动转发特定主题邮件"

## Requirements

### Software
- Python 3.10+ or appropriate runtime

## Best Practices

1. **使用HTML模板提升邮件美观度**
2. **批量操作时设置延迟避免频率限制**
3. **所有操作记录日志**

## Common Pitfalls

- ❌ 暴露SMTP密码(使用环境变量)
- ❌ 邮件频率过高触发spam过滤
- ❌ 忽视SSL/TLS加密要求

## Changelog

### v1.0.0
- Initial release from Qoder Skills Library
