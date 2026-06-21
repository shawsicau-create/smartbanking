---
name: openbb-finance
description: "Fetch financial data from OpenBB: stocks, options, crypto, macro."
workflow_stage: data
compatibility:
  - claude-code
  - cursor
  - codex
author: Qoder Skills Library
version: 1.0.0
tags:
  - finance
  - openbb
  - data
  - ai-integration
  - stocks
  - crypto
  - macro
---

# OpenBB Finance

## Purpose

Integrate OpenBB platform for comprehensive financial data retrieval and AI agent integration. Provides unified access to global financial markets including equities, options, cryptocurrency, fixed income, and macroeconomic indicators.

## When to Use

- Fetching stock price data and historical time series
- Retrieving options chains and implied volatility
- Accessing cryptocurrency market data
- Querying macroeconomic indicators and economic releases
- Getting fundamental financial statements and valuation metrics
- Building AI financial assistants with real-time data
- Trigger phrases: "OpenBB", "金融数据", "stock data", "market data", "crypto data"

## Instructions

### Step 1: Install OpenBB

Install the OpenBB platform:

```python
pip install openbb
```

For CLI interface:

```python
pip install openbb-cli
```

Requirements: Python 3.9 to 3.12

### Step 2: Initialize OpenBB

Import and initialize:

```python
from openbb import obb
# No API key required for many providers
# Optional: Set credentials for premium providers
```

### Step 3: Fetch Stock Data

Get historical prices:

```python
output = obb.equity.price.historical("AAPL")
df = output.to_dataframe()
```

Batch fetch multiple symbols:

```python
symbols = ["AAPL", "MSFT", "GOOGL"]
output = obb.equity.price.historical(symbols, start_date="2024-01-01")
```

### Step 4: Retrieve Options Data

Get options chain:

```python
output = obb.equity.options.chains("AAPL")
```

### Step 5: Access Macro Data

Get economic indicators:

```python
output = obb.economy.us_gdp()
```

### Step 6: Get Crypto Data

Fetch cryptocurrency prices:

```python
output = obb.crypto.price.historical("BTC-USD")
```

### Step 7: AI Integration Pattern

For AI agents, return structured data:

```python
from openbb import obb

def get_stock_analysis(symbol):
    output = obb.equity.price.historical(symbol, period="1y")
    df = output.to_dataframe()
    
    # Calculate key metrics
    latest_price = df['close'].iloc[-1]
    ytd_return = (df['close'].iloc[-1] / df['close'].iloc[0] - 1) * 100
    
    return {
        "symbol": symbol,
        "current_price": latest_price,
        "ytd_return_percent": round(ytd_return, 2),
        "data_points": len(df)
    }
```

### Step 8: Data Validation

Always check data quality:

```python
import pandas as pd

def validate_data(df):
    # Check for null values
    null_count = df.isnull().sum().sum()
    if null_count > 0:
        print(f"Warning: {null_count} null values found")
    
    # Check date range
    print(f"Date range: {df.index.min()} to {df.index.max()}")
    print(f"Total records: {len(df)}")
    
    return df
```

## Example Prompts

- "获取苹果公司最近一年的股价数据"
- "Fetch historical stock data for AAPL and MSFT"
- "查询最新的宏观经济指标"
- "Get options chain for TSLA"
- "分析比特币过去30天的价格趋势"
- "Build an AI stock analyzer using OpenBB"

## Requirements

### Software
- Python 3.9 to 3.12

### Packages
- `openbb` (core platform)
- `pandas` (data manipulation)
- `matplotlib` (optional, for visualization)

## Best Practices

1. **Handle rate limits** - Some providers have API rate limits
2. **Cache data** - Store fetched data locally to avoid repeated calls
3. **Validate dates** - Always specify date ranges clearly
4. **Use provider selection** - Choose appropriate data providers based on needs
5. **Error handling** - Wrap API calls in try-except blocks
6. **Data normalization** - Normalize data format across different providers

## Common Pitfalls

- ❌ Not checking if data is available for requested date range
- ❌ Assuming all data providers are free (some require API keys)
- ❌ Forgetting to convert OpenBB output to pandas DataFrame
- ❌ Ignoring timezone differences in market data
- ❌ Not validating data quality before analysis
- ❌ Using incompatible Python versions (< 3.9 or > 3.12)

## Additional Resources

- For detailed API documentation, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
- Utility scripts available in [scripts/](scripts/) directory

## Changelog

### v1.0.0
- Initial release
- Support for equities, options, crypto, and macro data
- AI agent integration patterns