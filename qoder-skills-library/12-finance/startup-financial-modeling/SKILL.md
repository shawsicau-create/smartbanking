---
name: startup-financial-modeling
description: "Build startup financial models: runway, fundraising, growth projections."
workflow_stage: analysis
compatibility:
  - claude-code
  - cursor
  - codex
author: Qoder Skills Library
version: 1.0.0
tags:
  - finance
  - startup
  - modeling
  - fundraising
---

# Startup Financial Modeling

## Purpose

为初创企业构建财务模型，包括跑道计算、融资情景分析和增长预测。适用于创业融资规划和初创企业财务诊断。

## When to Use

- 初创企业融资规划时使用
- 计算跑道和融资时间窗口时触发
- 增长预测和估值讨论时触发
- 触发词："创业财务"、"跑道"、"融资"、"startup model"

## Instructions

### Step 1
确认创业阶段：pre-seed/seed/Series A/B
### Step 2
构建财务模型：收入预测+支出预算+现金流
### Step 3
计算跑道：现有现金/月度净支出
### Step 4
模拟融资情景：不同估值/金额/稀释率
### Step 5
生成里程碑与融资时间线

## Example Prompts

- "计算6个月跑道和融资窗口"
- "模拟Series A不同估值情景"
- "预测18个月增长路径"

## Requirements

### Software
- Python 3.10+ or appropriate runtime

## Best Practices

1. **保守预测收入，激进估计支出**
2. **至少3种融资情景模拟**
3. **里程碑驱动而非时间驱动**

## Common Pitfalls

- ❌ 过度乐观的收入预测
- ❌ 忽视股权稀释累积效应
- ❌ 不预留应急缓冲

## Changelog

### v1.0.0
- Initial release from Qoder Skills Library
