---
name: finance-expert
description: Expert financial analysis framework combining accounting, valuation, and risk assessment for comprehensive financial research.
workflow_stage: analysis
compatibility:
  - claude-code
  - cursor
  - codex
author: Qoder Skills Library
version: 1.0.0
tags:
  - finance
  - accounting
  - valuation
  - risk
---

# Finance Expert

## Purpose

Provide expert-level financial analysis combining accounting fundamentals, valuation methodologies, and risk assessment frameworks. Designed for academic finance research and professional financial analysis that requires depth beyond surface-level metrics.

## When to Use

- Use this skill when you need comprehensive financial analysis beyond basic metrics
- This is especially helpful for academic research requiring rigorous analytical frameworks
- Trigger phrases: "financial analysis", "expert finance", "深度财务分析", "估值分析"

## Instructions

### Step 1: Framework Selection

Select appropriate analytical framework based on research question:
- **Valuation**: DCF, comparable company analysis, residual income
- **Risk**: Credit analysis, Altman Z-score, distance-to-default
- **Performance**: DuPont analysis, EVA, balanced scorecard

### Step 2: Data Collection and Preparation

Gather required financial data:
- Income statement, balance sheet, cash flow statement
- Market data (stock prices, beta, industry benchmarks)
- Macro data (interest rates, GDP growth, inflation)

### Step 3: Analysis Execution

Apply selected framework with proper methodology:
- Normalize financial data for comparability
- Compute key ratios and metrics
- Build models with explicit assumptions

### Step 4: Interpret and Report

Structure findings with:
- Key metrics summary table
- Sensitivity analysis on critical assumptions
- Limitations and caveats disclosure

## Example Prompts

- "Perform a DCF valuation of Apple Inc. with WACC calculation"
- "Analyze the credit risk of a Chinese bank using Altman Z-score"
- "Compare profitability metrics between tech and utility sectors"

## Requirements

### Software
- Python 3.10+, Excel, or R

### Packages
- `pandas`, `numpy`, `scipy` for quantitative analysis

## Best Practices

1. **State assumptions explicitly** — Every valuation model has assumptions; document them clearly
2. **Use multiple frameworks** — Cross-validate with at least 2 different methodologies
3. **Check data quality** — Financial statements may have accounting policy differences

## Common Pitfalls

- ❌ Using historical beta for forward-looking valuation without adjustment
- ❌ Ignoring accounting policy differences between companies
- ❌ Applying US-specific ratios to Chinese/other market companies without adaptation