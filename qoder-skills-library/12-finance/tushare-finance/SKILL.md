---
name: tushare-finance
description: Fetch Chinese A-share data via tushare Pro API for quant research.
workflow_stage: data
compatibility:
  - claude-code
  - cursor
  - codex
author: Qoder Skills Library
version: 1.0.0
tags:
  - finance
  - tushare
  - a-share
  - data
---

# Tushare Finance

## Purpose

通过tushare Pro API获取中国金融市场数据，支持A股研究、量化分析和金融数据获取。提供行情、财务、指数等多维度数据接口。

## When to Use

- 需要获取A股市场数据时使用
- tushare数据接口调用时触发
- 触发词："tushare"、"A股数据"、"金融数据获取"

## Instructions

### Step 1
确认数据需求：行情/财务/指数/资金流
### Step 2
调用tushare Pro API获取数据(需Token)
### Step 3
数据清洗：处理停牌、缺失值、复权
### Step 4
格式化输出为DataFrame
### Step 5
数据质量检查与异常标注

## Example Prompts

- "获取沪深300成分股列表"
- "下载贵州茅台近5年日线数据"
- "获取所有A股上市公司财务报表"

## Requirements

### Software
- Python 3.10+ or appropriate runtime

## Best Practices

1. **使用tushare Pro Token提高数据权限**
2. **按申万行业分类标准查询**
3. **注意数据更新频率差异**

## Common Pitfalls

- ❌ 未注册Pro Token导致数据限制
- ❌ 使用过时成分股列表(幸存者偏差)
- ❌ 忽视数据接口的调用频率限制

## Changelog

### v1.0.0
- Initial release from Qoder Skills Library
