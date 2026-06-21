---
name: financial-unit-economics
description: Calculate unit economics metrics (CAC, LTV, ARPU, payback period).
workflow_stage: analysis
compatibility:
  - claude-code
  - cursor
  - codex
author: Qoder Skills Library
version: 1.0.0
tags:
  - finance
  - unit-economics
  - saas
  - metrics
---

# Financial Unit Economics

## Purpose

计算和分析单位经济学指标(CAC/LTV/ARPU/回收期)，评估商业模式可行性和增长潜力。适用于SaaS和订阅制商业模式研究。

## When to Use

- 评估商业模式可行性时使用
- SaaS和订阅制业务分析时触发
- 需要计算CAC、LTV等关键指标时
- 触发词："单位经济学"、"CAC"、"LTV"、"ARPU"

## Instructions

### Step 1
确认业务模型类型：SaaS/电商/订阅/广告
### Step 2
定义单位维度：按客户/订单/用户
### Step 3
计算核心指标：CAC、LTV、ARPU、毛利率、回收期
### Step 4
评估LTV/CAC比率(理想>3:1)
### Step 5
做cohort分析追踪指标趋势

## Example Prompts

- "计算SaaS产品的LTV/CAC比率"
- "分析不同客户群的回收期差异"
- "评估ARPU增长对总营收的影响"

## Requirements

### Software
- Python 3.10+ or appropriate runtime

## Best Practices

1. **分cohort分析而非整体平均**
2. **区分付费用户和免费用户**
3. **包含客户流失率的影响**

## Common Pitfalls

- ❌ 混淆收入和利润指标
- ❌ 忽视客户流失对LTV的影响
- ❌ CAC包含不可归因的营销支出

## Changelog

### v1.0.0
- Initial release from Qoder Skills Library
