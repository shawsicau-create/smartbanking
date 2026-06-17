---
name: backtesting-trading-strategies
description: Backtest quantitative trading strategies against historical market data with performance metrics and risk analysis.
workflow_stage: analysis
compatibility:
  - claude-code
  - cursor
  - codex
author: Qoder Skills Library
version: 1.0.0
tags:
  - finance
  - trading
  - backtesting
  - quantitative
---

# Backtesting Trading Strategies

## Purpose

Backtest quantitative trading strategies against historical market data, computing key performance metrics (returns, Sharpe ratio, drawdown) and generating risk analysis reports. Designed for finance researchers and quant traders who need to validate strategy hypotheses before live deployment.

## When to Use

- Use this skill when you need to backtest a trading strategy against historical data
- This is especially helpful for validating strategy hypotheses, comparing multiple strategies, or generating academic-quality performance reports
- Trigger phrases: "backtest strategy", "回测", "strategy validation", "performance metrics"

## Instructions

### Step 1: Define the Strategy

Ask the user:
- What is the trading strategy logic? (entry/exit rules, position sizing)
- What asset(s) and time period to test?
- What data source? (Yahoo Finance API, local CSV, tushare)

### Step 2: Acquire Data

Fetch historical price data:
- Use `yfinance` or `tushare` for Chinese markets
- Validate data quality (missing values, survivorship bias)

### Step 3: Implement Strategy Logic

Write Python code using vectorized backtesting:
- Signal generation based on strategy rules
- Position tracking and trade execution simulation
- Transaction cost modeling

### Step 4: Compute Performance Metrics

Calculate standard metrics:
- Total return, annualized return
- Sharpe ratio, Sortino ratio
- Maximum drawdown, drawdown duration
- Win rate, profit factor
- Benchmark comparison (buy-and-hold)

### Step 5: Generate Report

Output a structured backtest report with:
- Equity curve plot
- Performance summary table
- Risk decomposition analysis

## Example Prompts

- "Backtest a momentum strategy on S&P 500 stocks from 2020-2025"
- "回测我的均线交叉策略在A股上的表现"
- "Compare MACD vs RSI strategy performance"

## Requirements

### Software
- Python 3.10+

### Packages
- `pandas`, `numpy`, `yfinance`, `matplotlib`, `backtrader` or vectorbt

## Best Practices

1. **Avoid survivorship bias** — Use point-in-time data, not current index constituents
2. **Model transaction costs** — Include realistic slippage and commission
3. **Use walk-forward validation** — Don't optimize on the same data you test on

## Common Pitfalls

- ❌ Ignoring transaction costs (overstates returns by 1-3% annually)
- ❌ Using future data in signal generation (look-ahead bias)
- ❌ Overfitting to a single time period

## Changelog

### v1.0.0
- Initial release from Qoder Skills Library