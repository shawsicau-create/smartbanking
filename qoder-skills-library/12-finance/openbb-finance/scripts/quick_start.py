"""
OpenBB Quick Start Guide
A simple script to get started with OpenBB.
"""
from openbb import obb
import pandas as pd


def quick_start_example():
    """Run a quick start example."""
    print("=" * 70)
    print("OpenBB Quick Start Guide")
    print("=" * 70)
    print()
    
    # Example 1: Get single stock data
    print("Example 1: Fetch Stock Data")
    print("-" * 70)
    
    symbol = "AAPL"
    print(f"Fetching data for {symbol}...")
    
    try:
        output = obb.equity.price.historical(
            symbol=symbol,
            period="1y"  # Last year
        )
        df = output.to_dataframe()
        
        if len(df) > 0:
            print(f"✓ Successfully fetched {len(df)} records")
            print()
            print(f"Data Summary:")
            print(f"  Symbol: {symbol}")
            print(f"  Date Range: {df.index.min().date()} to {df.index.max().date()}")
            print(f"  Current Price: ${df['close'].iloc[-1]:.2f}")
            print(f"  YTD Return: {(df['close'].iloc[-1] / df['close'].iloc[0] - 1) * 100:+.2f}%")
            print(f"  Average Volume: {df['volume'].mean():,.0f}")
            print()
            print(f"Last 5 rows:")
            print(df.tail().to_string())
        else:
            print(f"✗ No data found for {symbol}")
            
    except Exception as e:
        print(f"✗ Error fetching data: {e}")
        print("  Make sure OpenBB is installed: pip install openbb")
    
    print()
    print("=" * 70)
    
    # Example 2: Get multiple stocks
    print("\nExample 2: Batch Fetch Multiple Stocks")
    print("-" * 70)
    
    symbols = ["AAPL", "MSFT", "GOOGL"]
    print(f"Fetching data for: {', '.join(symbols)}")
    print()
    
    stock_data = []
    for sym in symbols:
        try:
            output = obb.equity.price.historical(sym, period="1y")
            df = output.to_dataframe()
            
            if len(df) > 0:
                current_price = df['close'].iloc[-1]
                ytd_return = (df['close'].iloc[-1] / df['close'].iloc[0] - 1) * 100
                
                stock_data.append({
                    "Symbol": sym,
                    "Price": f"${current_price:.2f}",
                    "YTD Return": f"{ytd_return:+.2f}%",
                    "52W High": f"${df['high'].max():.2f}",
                    "52W Low": f"${df['low'].min():.2f}"
                })
                
                print(f"✓ {sym}: ${current_price:.2f} (YTD: {ytd_return:+.2f}%)")
            else:
                print(f"✗ No data for {sym}")
                
        except Exception as e:
            print(f"✗ Error for {sym}: {e}")
    
    if stock_data:
        print()
        print("Summary Table:")
        summary_df = pd.DataFrame(stock_data)
        print(summary_df.to_string(index=False))
    
    print()
    print("=" * 70)
    
    # Example 3: Get crypto data
    print("\nExample 3: Fetch Cryptocurrency Data")
    print("-" * 70)
    
    crypto_symbol = "BTC-USD"
    print(f"Fetching Bitcoin data...")
    
    try:
        output = obb.crypto.price.historical(
            symbol=crypto_symbol,
            period="30d"
        )
        df = output.to_dataframe()
        
        if len(df) > 0:
            print(f"✓ Successfully fetched {len(df)} records")
            print()
            print(f"Bitcoin 30-Day Summary:")
            print(f"  Current Price: ${df['close'].iloc[-1]:,.2f}")
            print(f"  30-Day Return: {(df['close'].iloc[-1] / df['close'].iloc[0] - 1) * 100:+.2f}%")
            print(f"  30-Day High: ${df['high'].max():,.2f}")
            print(f"  30-Day Low: ${df['low'].min():,.2f}")
            print(f"  Average Volume: ${df['volume'].mean():,.0f}")
        else:
            print(f"✗ No data found for {crypto_symbol}")
            
    except Exception as e:
        print(f"✗ Error fetching crypto data: {e}")
    
    print()
    print("=" * 70)
    
    # Example 4: Get macro data
    print("\nExample 4: Fetch Macroeconomic Data")
    print("-" * 70)
    
    print("Fetching US GDP data...")
    
    try:
        output = obb.economy.us_gdp()
        gdp_df = output.to_dataframe()
        
        if len(gdp_df) > 0:
            print(f"✓ Successfully fetched GDP data")
            print()
            print(f"Latest GDP Growth: {gdp_df['value'].iloc[-1]:.2f}%")
            print(f"Date Range: {gdp_df.index.min()} to {gdp_df.index.max()}")
            print(f"Total Records: {len(gdp_df)}")
        else:
            print("✗ No GDP data found")
            
    except Exception as e:
        print(f"✗ Error fetching macro data: {e}")
    
    print()
    print("=" * 70)
    print("\nQuick Start Complete!")
    print("=" * 70)
    
    # Next steps
    print("\nNext Steps:")
    print("-" * 70)
    print("1. Explore more data types:")
    print("   - Options: obb.equity.options.chains('AAPL')")
    print("   - Fundamentals: obb.equity.fundamental.income('AAPL')")
    print("   - News: obb.news.company('AAPL')")
    print()
    print("2. Add technical analysis:")
    print("   - Install: pip install pandas-ta")
    print("   - Use: import pandas_ta as ta")
    print("   - Example: df['sma_20'] = ta.sma(df['close'], length=20)")
    print()
    print("3. Build custom functions:")
    print("   - Create reusable functions for your workflows")
    print("   - Combine multiple data sources")
    print("   - Generate reports and visualizations")
    print()
    print("4. For AI integration:")
    print("   - See ai_integration_example.py")
    print("   - Use structured data formats")
    print("   - Implement error handling")
    print()
    print("For more examples, see examples.md")
    print("=" * 70)


def simple_stock_query(symbol: str = "AAPL", period: str = "1y"):
    """
    Simple function to get stock data.
    
    Args:
        symbol: Stock ticker symbol
        period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
    
    Returns:
        Dictionary with stock summary
    """
    try:
        output = obb.equity.price.historical(symbol, period=period)
        df = output.to_dataframe()
        
        if len(df) == 0:
            return {"error": "No data available"}
        
        return {
            "symbol": symbol,
            "current_price": round(df['close'].iloc[-1], 2),
            "period_high": round(df['high'].max(), 2),
            "period_low": round(df['low'].min(), 2),
            "period_return_percent": round(
                (df['close'].iloc[-1] / df['close'].iloc[0] - 1) * 100, 2
            ),
            "volume": int(df['volume'].mean()),
            "data_points": len(df)
        }
        
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # Run the quick start example
    quick_start_example()
    
    # Example: Quick stock query
    print("\n" + "=" * 70)
    print("Quick Stock Query Example")
    print("=" * 70)
    result = simple_stock_query("AAPL")
    print(result)