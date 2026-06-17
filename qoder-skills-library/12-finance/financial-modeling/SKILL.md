---
name: financial-modeling
description: Build and analyze financial models including DCF, LBO, M&A, and budget projection models.
workflow_stage: analysis
compatibility:
  - claude-code
  - cursor
  - codex
author: Qoder Skills Library
version: 1.0.0
tags:
  - finance
  - modeling
  - DCF
  - valuation
---

# Financial Modeling

## Purpose

构建和分析金融模型，包括DCF估值、LBO杠杆收购、M&A并购和预算预测模型。适用于学术金融研究和专业财务分析。

## When to Use

- 构建金融估值模型时使用
- 杠杆收购或并购分析时触发
- 预算预测和情景分析时触发
- 触发词："金融模型"、"DCF"、"LBO"、"估值模型"

## Instructions

### Step 1
明确模型类型：DCF/LBO/M&A/预算/情景分析
### Step 2
收集输入数据：财务报表、市场数据、行业基准
### Step 3
构建模型结构：假设层→计算层→输出层
### Step 4
进行敏感性分析和情景测试
### Step 5
生成结构化模型报告与关键指标表

## Example Prompts

- "构建苹果公司的DCF估值模型"
- "分析杠杆收购案例的IRR"
- "预算未来3年营收增长率"

## Requirements

### Software
- Python 3.10+ or appropriate runtime

## Best Practices

1. **所有假设必须显式声明并文档化**
2. **使用至少3种情景(基准/乐观/悲观)**
3. **关键变量做敏感性分析**

## Common Pitfalls

- ❌ 隐藏假设导致模型不透明
- ❌ 使用单一情景做决策
- ❌ 忽略模型局限性

## Changelog

### v1.0.0
- Initial release from Qoder Skills Library
