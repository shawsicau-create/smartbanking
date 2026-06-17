---
name: finance-news
description: Fetch and analyze real-time financial news from multiple sources for market sentiment and event-driven research.
workflow_stage: data
compatibility:
  - claude-code
  - cursor
  - codex
author: Qoder Skills Library
version: 1.0.0
tags:
  - finance
  - news
  - sentiment
  - market
---

# Finance News

## Purpose

Fetch and analyze real-time financial news from multiple sources (Reuters, Bloomberg, Chinese financial media) for market sentiment analysis, event-driven research, and news-based trading strategy development. Provides structured news digestion and sentiment scoring.

## When to Use

- Use this skill when you need real-time financial news for market analysis
- This is especially helpful for event studies, sentiment analysis, and news-based strategy research
- Trigger phrases: "financial news", "市场新闻", "news sentiment", "财经新闻"

## Instructions

### Step 1: Define Scope

Ask the user:
- What market/asset/region? (US equities, China A-shares, crypto, etc.)
- What time window? (real-time, today, past week, past month)
- What focus? (earnings, M&A, regulatory, macro events)

### Step 2: Fetch News

Use WebSearch + WebFetch to gather news from:
- English: Reuters, Bloomberg, WSJ, Financial Times
- Chinese: 新浪财经, 东方财富, 第一财经, 证券时报

### Step 3: Analyze Sentiment

Score each news item:
- Sentiment: positive/neutral/negative (±1, 0)
- Relevance: high/medium/low
- Impact magnitude: minor/moderate/major

### Step 4: Synthesize Report

Generate structured summary:
- Key events timeline
- Sector-level sentiment heatmap
- Actionable implications for researchers/traders

## Example Prompts

- "获取今日A股市场重大新闻并分析情绪倾向"
- "Fetch recent US bank earnings news and assess market sentiment"
- "What are the key M&A events in Chinese tech sector this month?"

## Requirements

### Software
- Web browser (for news fetching)

## Best Practices

1. **Cross-validate sources** — Compare sentiment across English and Chinese sources
2. **Separate facts from opinions** — News contains both; distinguish them clearly
3. **Note time zone differences** — Chinese and US market hours differ significantly

## Common Pitfalls

- ❌ Confusing editorial opinion with factual reporting
- ❌ Ignoring Chinese market-specific regulatory language nuances
- ❌ Not accounting for after-hours news impact on next-day opening