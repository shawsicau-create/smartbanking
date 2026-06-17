# OpenBB API Reference

This document provides detailed reference for OpenBB core APIs and data providers.

## Core Object

```python
from openbb import obb
```

The `obb` object is the main interface for accessing all financial data.

## Equity Data

### Historical Price Data

```python
obb.equity.price.historical(
    symbol: str | List[str],
    start_date: str = None,
    end_date: str = None,
    provider: str = "yfinance",
    ...
)
```

**Parameters:**
- `symbol`: Stock ticker(s) (e.g., "AAPL" or ["AAPL", "MSFT"])
- `start_date`: Start date in YYYY-MM-DD format
- `end_date`: End date in YYYY-MM-DD format
- `provider`: Data provider (yfinance, intrinio, fmp, etc.)

**Returns:** OpenBB output object, convert with `.to_dataframe()`

**Example:**
```python
output = obb.equity.price.historical("AAPL", start_date="2024-01-01")
df = output.to_dataframe()
```

### Fundamental Data

```python
obb.equity.fundamental.income(
    symbol: str,
    period: str = "annual",
    provider: str = "yfinance"
)

obb.equity.fundamental.balance(
    symbol: str,
    period: str = "annual",
    provider: str = "yfinance"
)

obb.equity.fundamental.cash(
    symbol: str,
    period: str = "annual",
    provider: str = "yfinance"
)
```

**Parameters:**
- `symbol`: Stock ticker
- `period`: "annual" or "quarterly"
- `provider`: Data provider

### Price Targets and Analyst Ratings

```python
obb.equity.estimates.price_targets(
    symbol: str,
    provider: str = "intrinio"
)

obb.equity.estimates.ratings(
    symbol: str,
    provider: str = "intrinio"
)
```

### Company Information

```python
obb.equity.profile(
    symbol: str,
    provider: str = "yfinance"
)

obb.equity.ownership.insider_trading(
    symbol: str,
    provider: str = "intrinio"
)
```

## Options Data

### Options Chain

```python
obb.equity.options.chains(
    symbol: str,
    provider: str = "yfinance"
)
```

**Returns:** DataFrame with options chain data including strike, expiration, Greeks

### Implied Volatility

```python
obb.equity.options.iv(
    symbol: str,
    provider: str = "yfinance"
)
```

## Cryptocurrency

### Historical Price Data

```python
obb.crypto.price.historical(
    symbol: str,
    start_date: str = None,
    end_date: str = None,
    provider: str = "coinbase"
)
```

**Parameters:**
- `symbol`: Crypto pair (e.g., "BTC-USD", "ETH-USD")
- `start_date`: Start date in YYYY-MM-DD format
- `end_date`: End date in YYYY-MM-DD format

**Example:**
```python
output = obb.crypto.price.historical("BTC-USD", start_date="2024-01-01")
df = output.to_dataframe()
```

### Crypto Market Data

```python
obb.crypto.price.quote(
    symbol: str,
    provider: str = "coinbase"
)
```

## Macroeconomic Data

### US Economic Indicators

```python
obb.economy.us_gdp(provider: str = "fred")

obb.economy.us_cpi(provider: str = "fred")

obb.economy.us_unemployment(provider: str = "fred")

obb.economy.us_interest_rates(provider: str = "fred")
```

### Global Economic Data

```python
obb.economy.available_indicators(provider: str = "fred")
```

## Fixed Income

### Treasury Yields

```python
obb.fixedincome.treasury.yields(
    date: str = None,
    provider: str = "fred"
)
```

## News and Sentiment

### Company News

```python
obb.news.company(
    symbol: str,
    limit: int = 10,
    provider: str = "benzinga"
)
```

### Market News

```python
obb.news.world(
    limit: int = 10,
    provider: str = "benzinga"
)
```

## Technical Indicators

OpenBB returns raw price data. Use libraries like `ta` or `pandas-ta` for technical analysis:

```python
import pandas as pd
import pandas_ta as ta

# Calculate moving averages
df['sma_20'] = ta.sma(df['close'], length=20)
df['sma_50'] = ta.sma(df['close'], length=50)

# Calculate RSI
df['rsi'] = ta.rsi(df['close'], length=14)

# Calculate MACD
macd = ta.macd(df['close'])
df['macd'] = macd['MACD_12_26_9']
df['macd_signal'] = macd['MACDs_12_26_9']
```

## Data Providers

OpenBB supports multiple data providers:

| Provider | Type | API Key Required |
|----------|------|------------------|
| yfinance | Free | No |
| fmp | Free/Premium | Yes (for premium) |
| intrinio | Premium | Yes |
| coinbase | Free | No |
| fred | Free | No |
| benzinga | Premium | Yes |

**Select provider:**
```python
obb.equity.price.historical("AAPL", provider="yfinance")  # Free
obb.equity.estimates.price_targets("AAPL", provider="intrinio")  # Premium
```

## Output Format

All OpenBB functions return an OpenBB output object:

```python
output = obb.equity.price.historical("AAPL")

# Convert to pandas DataFrame
df = output.to_dataframe()

# Access raw data
data = output.results

# Display
print(output)
```

## Common DataFrame Columns

### Price Data
- `open`: Opening price
- `high`: Highest price
- `low`: Lowest price
- `close`: Closing price
- `volume`: Trading volume
- `vwap`: Volume weighted average price (if available)

### Options Data
- `strike`: Strike price
- `expiration`: Expiration date
- `call_put`: Call or Put
- `implied_volatility`: IV
- `greeks`: Option Greeks (delta, gamma, theta, vega)

## Error Handling

```python
try:
    output = obb.equity.price.historical("INVALID_TICKER")
    df = output.to_dataframe()
except Exception as e:
    print(f"Error fetching data: {e}")
```

## Best Practices

1. Always specify date ranges for historical data
2. Convert output to DataFrame immediately
3. Check for missing values
4. Use appropriate provider based on data needs
5. Handle rate limits gracefully
6. Cache frequently accessed data locally

## Additional Resources

- Official OpenBB Docs: https://docs.openbb.co
- API Reference: https://docs.openbb.co/api
- GitHub Repository: https://github.com/OpenBB-finance/OpenBB