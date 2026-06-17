---
name: china-stock-analysis
description: Analyze Chinese A-share market data using tushare and akshare APIs for quantitative research.
workflow_stage: analysis
compatibility:
  - claude-code
  - cursor
  - codex
author: Qoder Skills Library
version: 1.0.0
tags:
  - finance
  - china
  - stock
  - a-share
---

# China Stock Analysis

## Purpose

Analyze Chinese A-share market data for quantitative finance research. Provides comprehensive tools for fetching market data, computing financial metrics, and generating academic-quality analysis reports focused on the Chinese stock market.

## When to Use

- Use this skill when you need to analyze Chinese stock market data
- This is especially helpful for A-share specific research, market microstructure studies, and Chinese financial market comparisons
- Trigger phrases: "分析A股", "中国股票", "chinese stock market", "A股数据"

## Instructions

### Step 1: Acquire Data

Use tushare or akshare API to fetch:
- Stock price data (daily OHLCV)
- Financial statements (balance sheet, income statement)
- Market index data (CSI 300, CSI 500)

### Step 2: Compute Financial Metrics

Calculate standard metrics:
- PE ratio, PB ratio, ROE, EPS growth
- Market capitalization and turnover ratio
- Dividend yield and payout ratio

### Step 3: Generate Analysis Report

Output a structured report with:
- Market overview and sector breakdown
- Individual stock profiles with key metrics
- Comparative analysis tables

## Example Prompts

- "分析贵州茅台近5年的财务指标"
- "Compare CSI 300 vs CSI 500 performance in 2024"
- "获取沪深300成分股的市盈率分布"

## Requirements

### Software
- Python 3.10+

### Packages
- `tushare`, `akshare`, `pandas`, `matplotlib`

## Best Practices

1. **Handle trading calendar** — Chinese market has unique trading days (Spring Festival closure, National Day)
2. **Adjust for A-share specifics** — Price limits (±10%), T+1 rules, stamp duty
3. **Use sector classification** —申万行业分类标准 for consistent categorization

## Common Pitfalls

- ❌ Using US market conventions for Chinese data (different trading hours, settlement rules)
- ❌ Ignoring A-share price limits and special trading mechanisms
- ❌ Not accounting for different accounting standards (Chinese GAAP vs IFRS)