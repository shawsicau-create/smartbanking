"""
Apple (AAPL) 过去 3 年日度股价数据分析
=========================================
数据源：OpenBB Platform（默认 yfinance provider）/ yfinance 备选方案
功能：获取数据 → 整理 DataFrame → 计算日收益率/累计收益率/年化波动率 → 绘图

运行前请先安装依赖：
    pip install openbb pandas numpy matplotlib
    # 如需轻量备选方案：
    pip install yfinance pandas numpy matplotlib
"""

from datetime import datetime, timedelta
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")


# --------------------------------------------------
# 0. 全局配置
# --------------------------------------------------
plt.rcParams["font.sans-serif"] = [
    "PingFang SC", "Heiti SC", "Arial Unicode MS", "SimHei", "DejaVu Sans"
]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 120
plt.rcParams["font.size"] = 11

TRADING_DAYS = 252          # 年交易日数
SYMBOL = "AAPL"             # 股票代码
end_date = datetime.today().strftime("%Y-%m-%d")
start_date = (datetime.today() - timedelta(days=365 * 3)).strftime("%Y-%m-%d")

# ==================================================
# 1. 数据获取（OpenBB 主方案 / yfinance 备选）
# ==================================================
df = None
data_source = ""
use_openbb = True

print("=" * 60)
print(f"开始获取 {SYMBOL} 日度股价数据  ({start_date} ~ {end_date})")
print("=" * 60)

if use_openbb:
    try:
        from openbb import obb
        print(">> 正在使用 OpenBB Platform 获取数据 (provider: yfinance)...")
        result = obb.equity.price.historical(
            symbol=SYMBOL,
            start_date=start_date,
            end_date=end_date,
            provider="yfinance",   # 免费，无需 API key
        )
        df = result.to_df()
        data_source = "OpenBB Platform (provider: yfinance)"
        print(f">> OpenBB 获取成功，共 {len(df)} 条记录")
    except ImportError:
        print(">> 未检测到 OpenBB，自动切换至 yfinance 备选方案...")
        use_openbb = False
    except Exception as e:
        print(f">> OpenBB 获取失败：{e}")
        print(">> 自动切换至 yfinance 备选方案...")
        use_openbb = False

if not use_openbb:
    # 备选 1：yfinance 库
    try:
        import yfinance as yf
        print(">> 正在使用 yfinance 获取数据...")
        ticker = yf.Ticker(SYMBOL)
        df = ticker.history(start=start_date, end=end_date)
        data_source = "yfinance (备用方案)"
        print(f">> yfinance 获取成功，共 {len(df)} 条记录")
    except Exception as e:
        print(f">> yfinance 获取失败：{e}")
        df = None

    # 备选 2：requests 直连 Yahoo Finance Chart API（最可靠）
    if df is None:
        import requests
        import time as _time
        print(">> 正在通过 requests 直连 Yahoo Finance API 获取数据...")

        def _fetch_yahoo(symbol, start_dt, end_dt):
            """直接调用 Yahoo Finance Chart API 获取日度 OHLCV 数据"""
            period1 = int(start_dt.timestamp())
            period2 = int(end_dt.timestamp())
            url = "https://query1.finance.yahoo.com/v8/finance/chart/" + symbol
            params = {
                "period1": str(period1),
                "period2": str(period2),
                "interval": "1d",
                "events": "div,split",
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/120.0.0.0 Safari/537.36",
            }
            resp = requests.get(url, params=params,
                                headers=headers, timeout=30)
            resp.raise_for_status()
            raw = resp.json()["chart"]["result"][0]
            timestamps = raw["timestamp"]
            quote = raw["indicators"]["quote"][0]
            adjclose_list = raw["indicators"].get("adjclose", [{}])
            adjclose = adjclose_list[0].get(
                "adjclose", quote["close"]) if adjclose_list else quote["close"]

            records = []
            for i, ts in enumerate(timestamps):
                close_val = quote["close"][i]
                if close_val is None:
                    continue
                records.append({
                    "date": pd.Timestamp(ts, unit="s", tz="UTC").tz_localize(None),
                    "open": quote["open"][i],
                    "high": quote["high"][i],
                    "low": quote["low"][i],
                    "close": close_val,
                    "adjclose": adjclose[i] if i < len(adjclose) else close_val,
                    "volume": quote["volume"][i],
                })
            result_df = pd.DataFrame(records).set_index("date")
            return result_df

        df = _fetch_yahoo(SYMBOL, datetime.today() -
                          timedelta(days=365 * 3), datetime.today())
        data_source = "Yahoo Finance Chart API (requests 直连)"
        print(f">> requests 直连获取成功，共 {len(df)} 条记录")

# ==================================================
# 2. 数据整理为 pandas DataFrame
# ==================================================
df = df.sort_index()

# 确保 index 为 pandas Timestamp（OpenBB 可能返回 datetime.date）
df.index = pd.to_datetime(df.index)

# 统一列名为小写，方便后续操作
df.columns = [c.lower().replace(" ", "_") for c in df.columns]

# 如果存在 adjclose（后复权价），优先使用它作为收盘价
if "adjclose" in df.columns:
    df["close"] = df["adjclose"]

# 仅保留需要的列
needed = [c for c in ["open", "high", "low", "close", "volume",
                      "dividends", "stock_splits"] if c in df.columns]
df = df[needed].copy()

print(f"\n数据范围：{df.index.min().date()}  ~  {df.index.max().date()}")
print(f"交易日总数：{len(df)}")

# ==================================================
# 3. 指标计算
# ==================================================
# 3-1  日收益率
df["daily_return"] = df["close"].pct_change()

# 3-2  累计收益率
df["cumulative_return"] = (1 + df["daily_return"]).cumprod() - 1

# 3-3  年化波动率（日波动率 × √252）
annual_volatility = df["daily_return"].std() * np.sqrt(TRADING_DAYS)

# 补充统计指标
total_return = df["cumulative_return"].iloc[-1]
n_years = len(df) / TRADING_DAYS
annualized_return = (1 + total_return) ** (1 / n_years) - 1
max_drawdown = (df["close"] / df["close"].cummax() - 1).min()
rf_rate = 0.043                                  # 假设无风险利率 4.3%（1年期国债）
sharpe_ratio = (annualized_return - rf_rate) / annual_volatility

print(f"\n{'─' * 50}")
print(f"  关键统计指标  ( {SYMBOL} ，过去 {n_years:.1f} 年 )")
print(f"{'─' * 50}")
print(f"  累计总收益率:       {total_return:>10.2%}")
print(f"  年化收益率:         {annualized_return:>10.2%}")
print(f"  年化波动率:         {annual_volatility:>10.2%}")
print(f"  最大回撤:           {max_drawdown:>10.2%}")
print(f"  夏普比率 (rf={rf_rate:.1%}): {sharpe_ratio:>10.2f}")
print(f"{'─' * 50}")

print("\n数据预览（前 5 行）：")
print(df[["close", "daily_return", "cumulative_return"]].head().round(4))
print("\n数据预览（后 5 行）：")
print(df[["close", "daily_return", "cumulative_return"]].tail().round(4))

# ==================================================
# 4. 绘图：收盘价走势 + 累计收益率曲线
# ==================================================
fig, axes = plt.subplots(2, 1, figsize=(14, 9), sharex=True)

# --- 子图 1：收盘价走势 ---
axes[0].plot(df.index, df["close"], color="#1f77b4",
             linewidth=1.2, label="AAPL 收盘价")
axes[0].fill_between(df.index, df["close"].min() * 0.9, df["close"],
                     alpha=0.06, color="#1f77b4")
axes[0].set_title(f"Apple ({SYMBOL}) 收盘价走势  "
                  f"({start_date} ~ {end_date})", fontsize=14, fontweight="bold")
axes[0].set_ylabel("收盘价 (USD)")
axes[0].legend(loc="upper left")
axes[0].grid(True, alpha=0.3)

# --- 子图 2：累计收益率 ---
cum_pct = df["cumulative_return"] * 100
axes[1].plot(df.index, cum_pct, color="#2ca02c", linewidth=1.2, label="累计收益率")
axes[1].axhline(y=0, color="red", linestyle="--", linewidth=0.8, alpha=0.5)
axes[1].fill_between(df.index, 0, cum_pct, alpha=0.08, color="#2ca02c")
axes[1].set_title("累计收益率曲线", fontsize=14, fontweight="bold")
axes[1].set_ylabel("累计收益率 (%)")
axes[1].set_xlabel("日期")
axes[1].legend(loc="upper left")
axes[1].grid(True, alpha=0.3)

# X 轴日期格式
axes[1].xaxis.set_major_locator(mdates.MonthLocator(interval=3))
axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45, ha="right")

plt.tight_layout()
chart_path = "aapl_analysis_chart.png"
plt.savefig(chart_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"\n图表已保存：{chart_path}")

# 保存完整数据为 CSV
csv_path = "aapl_daily_data.csv"
df.to_csv(csv_path)
print(f"数据已保存：{csv_path}")

# ==================================================
# 5. 数据来源说明
# ==================================================
print(f"""
{'=' * 60}
  数据来源与局限性说明
{'=' * 60}
  数据来源：  {data_source}
  数据频率：  日度（仅交易日；周末和节假日不含在内）
  价格类型：  后复权收盘价（Adjusted Close）
              — 已考虑股票拆分、合并和股息再投资因素

  局限性：
  1) 历史收益率不代表未来表现，以上分析仅用于回顾；
  2) 年化波动率假设日收益独立同分布（i.i.d.），
     未刻画金融时间序列中常见的"波动率聚集"（GARCH 效应）；
  3) 夏普比率中的无风险利率假设为固定 {rf_rate:.1%}，实际中该利率
     在 3 年区间内会有变动；
  4) yfinance 属于免费数据源，数据质量通常低于付费终端
     （如 Bloomberg、Refinitiv），极端行情下可能存在缺失或延迟；
  5) 数据仅覆盖美股正常交易时段（09:30–16:00 ET），
     不含盘前/盘后交易。
{'=' * 60}
""")
