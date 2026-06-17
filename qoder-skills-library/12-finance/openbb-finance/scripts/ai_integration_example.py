"""
OpenBB AI Integration Example
Demonstrates how to integrate OpenBB with AI agents for financial analysis.
"""
from openbb import obb
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta


class FinancialDataAgent:
    """
    AI Agent for financial data retrieval and analysis.
    Provides structured data for AI-powered financial applications.
    """
    
    def __init__(self):
        """Initialize the financial data agent."""
        self.obb = obb
        self.cache = {}
    
    def get_stock_summary(self, symbol: str, period: str = "1y") -> Dict[str, Any]:
        """
        Get comprehensive stock summary for AI analysis.
        
        Args:
            symbol: Stock ticker symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        
        Returns:
            Dictionary with structured stock data and metrics
        """
        try:
            # Fetch historical data
            output = self.obb.equity.price.historical(symbol, period=period)
            df = output.to_dataframe()
            
            if len(df) == 0:
                return {
                    "symbol": symbol,
                    "status": "error",
                    "message": "No data available"
                }
            
            # Calculate key metrics
            current_price = df['close'].iloc[-1]
            period_return = (df['close'].iloc[-1] / df['close'].iloc[0] - 1) * 100
            
            # Calculate volatility
            daily_returns = df['close'].pct_change()
            volatility = daily_returns.std() * (252**0.5)  # Annualized
            
            # Calculate moving averages
            sma_20 = df['close'].rolling(window=20).mean().iloc[-1]
            sma_50 = df['close'].rolling(window=50).mean().iloc[-1]
            
            # Support and resistance levels
            support = df['low'].tail(20).min()
            resistance = df['high'].tail(20).max()
            
            # Generate signal
            signal = self._generate_signal(current_price, sma_20, sma_50)
            
            return {
                "symbol": symbol,
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "price_data": {
                    "current_price": round(current_price, 2),
                    "period_high": round(df['high'].max(), 2),
                    "period_low": round(df['low'].min(), 2),
                    "period_return_percent": round(period_return, 2),
                    "volatility": round(volatility, 4)
                },
                "technical_indicators": {
                    "sma_20": round(sma_20, 2),
                    "sma_50": round(sma_50, 2),
                    "support_level": round(support, 2),
                    "resistance_level": round(resistance, 2),
                    "price_vs_sma20_pct": round((current_price / sma_20 - 1) * 100, 2),
                    "price_vs_sma50_pct": round((current_price / sma_50 - 1) * 100, 2)
                },
                "trading_signal": signal,
                "risk_metrics": {
                    "max_drawdown": round(
                        (df['close'].max() - df['close'].min()) / df['close'].max() * 100, 2
                    ),
                    "average_volume": int(df['volume'].mean()),
                    "data_points": len(df)
                }
            }
            
        except Exception as e:
            return {
                "symbol": symbol,
                "status": "error",
                "message": str(e)
            }
    
    def _generate_signal(self, price: float, sma_20: float, sma_50: float) -> Dict[str, str]:
        """Generate trading signal based on price and moving averages."""
        if price > sma_20 > sma_50:
            return {
                "direction": "LONG",
                "strength": "STRONG",
                "reasoning": "Price above both SMAs with uptrend"
            }
        elif price > sma_20:
            return {
                "direction": "LONG",
                "strength": "MODERATE",
                "reasoning": "Price above SMA-20"
            }
        elif price < sma_20 < sma_50:
            return {
                "direction": "SHORT",
                "strength": "STRONG",
                "reasoning": "Price below both SMAs with downtrend"
            }
        elif price < sma_20:
            return {
                "direction": "SHORT",
                "strength": "MODERATE",
                "reasoning": "Price below SMA-20"
            }
        else:
            return {
                "direction": "NEUTRAL",
                "strength": "WEAK",
                "reasoning": "Price between SMAs"
            }
    
    def compare_stocks(self, symbols: List[str], period: str = "1y") -> Dict[str, Any]:
        """
        Compare multiple stocks side by side.
        
        Args:
            symbols: List of stock symbols
            period: Time period
        
        Returns:
            Dictionary with comparison results
        """
        results = []
        
        for symbol in symbols:
            summary = self.get_stock_summary(symbol, period)
            results.append(summary)
        
        # Sort by period return
        results.sort(
            key=lambda x: x.get('price_data', {}).get('period_return_percent', 0),
            reverse=True
        )
        
        return {
            "comparison_type": "performance_comparison",
            "period": period,
            "symbols_analyzed": len(symbols),
            "timestamp": datetime.now().isoformat(),
            "results": results
        }
    
    def get_market_sentiment(self, indices: List[str] = None) -> Dict[str, Any]:
        """
        Get overall market sentiment using major indices.
        
        Args:
            indices: List of index symbols (default: SPY, QQQ, IWM)
        
        Returns:
            Dictionary with market sentiment analysis
        """
        if indices is None:
            indices = ["SPY", "QQQ", "IWM"]  # S&P 500, Nasdaq-100, Russell 2000
        
        results = []
        positive_count = 0
        negative_count = 0
        
        for index in indices:
            summary = self.get_stock_summary(index, period="5d")
            
            if summary.get("status") == "success":
                returns = summary['price_data']['period_return_percent']
                if returns > 0:
                    positive_count += 1
                else:
                    negative_count += 1
                
                results.append({
                    "index": index,
                    "return_percent": returns,
                    "signal": summary['trading_signal']
                })
        
        # Determine overall sentiment
        total = positive_count + negative_count
        if total == 0:
            sentiment = "NEUTRAL"
        elif positive_count / total > 0.66:
            sentiment = "BULLISH"
        elif negative_count / total > 0.66:
            sentiment = "BEARISH"
        else:
            sentiment = "MIXED"
        
        return {
            "market_sentiment": sentiment,
            "positive_indices": positive_count,
            "negative_indices": negative_count,
            "total_indices": total,
            "timestamp": datetime.now().isoformat(),
            "index_performance": results
        }
    
    def generate_financial_report(self, symbol: str, period: str = "1y") -> str:
        """
        Generate a natural language financial report for AI consumption.
        
        Args:
            symbol: Stock symbol
            period: Time period
        
        Returns:
            Formatted text report
        """
        data = self.get_stock_summary(symbol, period)
        
        if data.get("status") != "success":
            return f"Unable to generate report for {symbol}: {data.get('message')}"
        
        price_data = data['price_data']
        tech_indicators = data['technical_indicators']
        signal = data['trading_signal']
        risk_metrics = data['risk_metrics']
        
        report = f"""
Financial Analysis Report: {symbol}
{'=' * 50}

PERFORMANCE SUMMARY
-------------------
Current Price: ${price_data['current_price']}
Period Return: {price_data['period_return_percent']:+.2f}%
Period High: ${price_data['period_high']}
Period Low: ${price_data['period_low']}
Volatility: {price_data['volatility']:.2%}

TECHNICAL ANALYSIS
------------------
SMA-20: ${tech_indicators['sma_20']}
SMA-50: ${tech_indicators['sma_50']}
Support Level: ${tech_indicators['support_level']}
Resistance Level: ${tech_indicators['resistance_level']}

Price Position: {tech_indicators['price_vs_sma50_pct']:+.2f}% from SMA-50

TRADING SIGNAL
--------------
Direction: {signal['direction']}
Strength: {signal['strength']}
Reasoning: {signal['reasoning']}

RISK METRICS
------------
Max Drawdown: {risk_metrics['max_drawdown']}%
Average Volume: {risk_metrics['average_volume']:,.0f}
Data Points: {risk_metrics['data_points']}

SUMMARY
-------
{'Bullish' if signal['direction'] == 'LONG' else 'Bearish'} outlook with {signal['strength']} strength.
{'Consider buying opportunities' if signal['direction'] == 'LONG' else 'Consider selling or avoiding' if signal['direction'] == 'SHORT' else 'Hold current position'}.

Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return report


def ai_assistant_example():
    """Example of AI assistant using OpenBB data."""
    print("=" * 70)
    print("OpenBB AI Assistant Example")
    print("=" * 70)
    print()
    
    # Initialize agent
    agent = FinancialDataAgent()
    
    # Example 1: Get stock analysis
    print("1. Stock Analysis")
    print("-" * 70)
    
    stock = "AAPL"
    analysis = agent.get_stock_summary(stock)
    
    if analysis.get("status") == "success":
        print(f"✓ {stock} Analysis Complete")
        print(f"  Current Price: ${analysis['price_data']['current_price']}")
        print(f"  Period Return: {analysis['price_data']['period_return_percent']:+.2f}%")
        print(f"  Signal: {analysis['trading_signal']['direction']} ({analysis['trading_signal']['strength']})")
        print(f"  Reasoning: {analysis['trading_signal']['reasoning']}")
    else:
        print(f"✗ Analysis failed: {analysis.get('message')}")
    
    print()
    
    # Example 2: Compare stocks
    print("2. Stock Comparison")
    print("-" * 70)
    
    symbols = ["AAPL", "MSFT", "GOOGL"]
    comparison = agent.compare_stocks(symbols)
    
    print(f"Comparison of {len(symbols)} stocks:")
    print()
    print(f"{'Symbol':<10} {'Price':<10} {'Return':<10} {'Signal':<10}")
    print("-" * 40)
    
    for result in comparison['results']:
        if result.get("status") == "success":
            price = result['price_data']['current_price']
            returns = result['price_data']['period_return_percent']
            signal = result['trading_signal']['direction']
            
            print(f"{result['symbol']:<10} ${price:<9.2f} {returns:+9.2f}% {signal:<10}")
    
    print()
    
    # Example 3: Market sentiment
    print("3. Market Sentiment")
    print("-" * 70)
    
    sentiment = agent.get_market_sentiment()
    
    print(f"Overall Market Sentiment: {sentiment['market_sentiment']}")
    print(f"Positive Indices: {sentiment['positive_indices']}")
    print(f"Negative Indices: {sentiment['negative_indices']}")
    print()
    
    for index_data in sentiment['index_performance']:
        idx = index_data['index']
        ret = index_data['return_percent']
        sig = index_data['signal']['direction']
        print(f"  {idx}: {ret:+.2f}% ({sig})")
    
    print()
    
    # Example 4: Generate financial report
    print("4. Financial Report")
    print("-" * 70)
    
    report = agent.generate_financial_report("AAPL")
    print(report)
    
    print("=" * 70)
    print("AI Assistant Example Complete")
    print("=" * 70)


def natural_language_query(query: str) -> Dict[str, Any]:
    """
    Process natural language queries about financial data.
    Example AI integration pattern.
    
    Args:
        query: Natural language query (e.g., "how is Apple stock doing?")
    
    Returns:
        Structured response
    """
    agent = FinancialDataAgent()
    query_lower = query.lower()
    
    # Parse query and route to appropriate function
    if "apple" in query_lower or "aapl" in query_lower:
        symbol = "AAPL"
    elif "microsoft" in query_lower or "msft" in query_lower:
        symbol = "MSFT"
    elif "google" in query_lower or "googl" in query_lower:
        symbol = "GOOGL"
    elif "tesla" in query_lower or "tsla" in query_lower:
        symbol = "TSLA"
    else:
        return {
            "status": "error",
            "message": "Symbol not recognized in query"
        }
    
    # Get data
    data = agent.get_stock_summary(symbol)
    
    # Generate natural language response
    if data.get("status") == "success":
        price = data['price_data']['current_price']
        returns = data['price_data']['period_return_percent']
        signal = data['trading_signal']['direction']
        strength = data['trading_signal']['strength']
        
        response = {
            "status": "success",
            "symbol": symbol,
            "summary": f"{symbol} is currently trading at ${price:.2f}",
            "performance": f"The stock has {('gained' if returns > 0 else 'lost')} {abs(returns):.2f}% over the past year",
            "outlook": f"The technical analysis indicates a {strength.lower()} {signal.lower()} signal",
            "detailed_data": data
        }
    else:
        response = {
            "status": "error",
            "message": data.get("message")
        }
    
    return response


if __name__ == "__main__":
    # Run AI assistant example
    ai_assistant_example()
    
    # Example: Natural language query
    print("\n" + "=" * 70)
    print("Natural Language Query Example")
    print("=" * 70)
    
    query = "How is Apple stock doing?"
    print(f"\nQuery: {query}\n")
    
    response = natural_language_query(query)
    
    if response.get("status") == "success":
        print(response['summary'])
        print(response['performance'])
        print(response['outlook'])
    else:
        print(f"Error: {response.get('message')}")
    
    print("\n" + "=" * 70)