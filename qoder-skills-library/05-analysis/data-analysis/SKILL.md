---
name: data-analysis
description: Exploratory data analysis, statistical testing, and pattern discovery.
workflow_stage: analysis
compatibility:
  - claude-code
  - cursor
  - codex
author: Qoder Skills Library
version: 1.0.0
tags:
  - analysis
  - eda
  - statistics
  - data
---

# Data Analysis

## Purpose

执行探索性数据分析、统计检验和模式发现，从研究数据中提取洞察。适用于数据驱动的研究分析。

## When to Use

- 对数据集进行探索性分析时使用
- 需要统计检验和模式发现时触发
- 触发词："数据分析"、"EDA"、"统计检验"

## Instructions

### Step 1
确认数据类型和分析目标
### Step 2
数据概览：描述统计、分布、缺失值
### Step 3
EDA：可视化分布、相关性、异常值
### Step 4
统计检验：t-test、ANOVA、chi-square
### Step 5
模式发现：聚类、降维、关联规则

## Example Prompts

- "对调查数据进行EDA分析"
- "检验两组数据是否存在显著差异"
- "发现数据中的聚类模式"

## Requirements

### Software
- Python 3.10+ or appropriate runtime

## Best Practices

1. **先EDA再建模**
2. **标注统计显著性和效应量**
3. **区分探索性和验证性分析**

## Common Pitfalls

- ❌ 过度拟合EDA发现的模式
- ❌ 忽视数据质量问题
- ❌ 混淆相关和因果

## Changelog

### v1.0.0
- Initial release from Qoder Skills Library
