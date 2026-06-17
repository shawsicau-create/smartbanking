---
name: stock-analysis
description: Perform comprehensive stock analysis with technical, fundamental, and quantitative approaches for investment research.
workflow_stage: analysis
compatibility:
  - claude-code
  - cursor
  - codex
author: Qoder Skills Library
version: 1.0.0
tags:
  - finance
  - stock
  - technical-analysis
  - fundamental
---

# Stock Analysis

## Purpose

执行综合股票分析，结合技术分析、基本面分析和量化方法。适用于投资研究和学术论文中的金融市场分析。

## When to Use

- 对个股进行综合分析时使用
- 需要技术面+基本面+量化三维度分析时触发
- 触发词："股票分析"、"个股研究"、"stock analysis"

## Instructions

### Step 1
确认分析目标：个股深度研究 vs 行业横向对比
### Step 2
基本面分析：财务指标、估值倍数、盈利质量
### Step 3
技术面分析：趋势识别、支撑阻力、成交量
### Step 4
量化分析：因子评分、风险指标、回测验证
### Step 5
综合评分与投资建议生成

## Example Prompts

- "综合分析苹果股票的投资价值"
- "技术面+基本面双维度评估"
- "对比科技板块估值分布"

## Requirements

### Software
- Python 3.10+ or appropriate runtime

## Best Practices

1. **基本面和技术面交叉验证**
2. **使用多个估值方法(PE/PB/DCF)**
3. **标注数据来源和时间**

## Common Pitfalls

- ❌ 只用单一分析方法
- ❌ 忽视宏观环境影响
- ❌ 混淆价格和内在价值

## Changelog

### v1.0.0
- Initial release from Qoder Skills Library
