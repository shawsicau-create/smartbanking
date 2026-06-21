---
name: saas-economics-efficiency-metrics
description: "Analyze SaaS metrics: Rule of 40, burn multiple, net retention."
workflow_stage: analysis
compatibility:
  - claude-code
  - cursor
  - codex
author: Qoder Skills Library
version: 1.0.0
tags:
  - finance
  - saas
  - efficiency
  - rule-of-40
---

# Saas Economics Efficiency Metrics

## Purpose

分析SaaS特有效率指标(Rule of 40、燃烧倍数、回收期、净留存率)，评估增长阶段企业的运营效率和资本利用效率。

## When to Use

- 评估SaaS公司增长效率时使用
- 需要Rule of 40等SaaS专用指标时触发
- 增长阶段企业对比分析时触发
- 触发词："SaaS指标"、"Rule of 40"、"燃烧倍数"、"净留存率"

## Instructions

### Step 1
确认评估目标：单公司诊断 vs 行业对比
### Step 2
获取关键SaaS指标数据：ARR、NRR、毛利率、增长率
### Step 3
计算效率指标：Rule of 40(增长率+毛利率≥40%)、燃烧倍数
### Step 4
对标行业基准(Bessemer SaaS指数)
### Step 5
生成效率评分与发展阶段诊断

## Example Prompts

- "评估SaaS公司的Rule of 40达标情况"
- "计算燃烧倍数判断资本效率"
- "对比SaaS行业的NRR基准"

## Requirements

### Software
- Python 3.10+ or appropriate runtime

## Best Practices

1. **按发展阶段分层评估(早期/增长/成熟)**
2. **使用可比公司基准而非绝对值**
3. **区分GAAP和非GAAP指标**

## Common Pitfalls

- ❌ 用GAAP毛利率替代SaaS毛利率
- ❌ 忽视合同结构差异(MRR vs ARR)
- ❌ 混淆增长率和净增长率

## Changelog

### v1.0.0
- Initial release from Qoder Skills Library
