---
name: yahoo-finance
description: Fetch global market data via yfinance for cross-border analysis.
workflow_stage: data
compatibility:
  - claude-code
  - cursor
  - codex
author: Qoder Skills Library
version: 1.0.0
tags:
  - finance
  - yahoo
  - data
  - international
---

# Yahoo Finance

## Purpose

通过yfinance API获取全球金融市场数据，支持国际市场研究、跨境对比分析和全球资产配置研究。覆盖美股、港股、A股等主要市场。

## When to Use

- 需要获取全球市场数据时使用
- 美股港股数据获取时触发
- 触发词："yahoo finance"、"yfinance"、"美股数据"

## Instructions

### Step 1
确认目标市场和 ticker 代码
### Step 2
使用yfinance下载OHLCV数据和财务报表
### Step 3
处理数据：汇率转换、时区对齐
### Step 4
计算技术指标和基本面比率
### Step 5
生成数据摘要和可视化

## Example Prompts

- "下载苹果公司近5年股票数据"
- "获取标普500成分股PE分布"
- "对比美股和A股银行板块估值"

## Requirements

### Software
- Python 3.10+ or appropriate runtime

## Best Practices

1. **确认ticker代码格式(美股/A股/港股不同)**
2. **注意汇率和时区差异**
3. **交叉验证关键数据**

## Common Pitfalls

- ❌ ticker格式错误(如A股需加.SS/.SZ)
- ❌ 忽视交易时间差异
- ❌ 财务数据可能延迟更新

## Changelog

### v1.0.0
- Initial release from Qoder Skills Library
