import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 1) Choose a stock ticker (examples: AAPL, MSFT, JPM, TSLA, NVDA)
TICKER = "AAPL"

# 2) Download last 2 years of daily data
df = yf.download(TICKER, period="2y", interval="1d", auto_adjust=True)

# Safety check
if df.empty:
    raise ValueError("No data returned. Check your internet connection or ticker symbol.")

# 3) Keep only what we need
df = df[["Close"]].copy()

# 4) Indicators
df["MA20"] = df["Close"].rolling(window=20).mean()
df["MA50"] = df["Close"].rolling(window=50).mean()
df["DailyReturn"] = df["Close"].pct_change()
df["Volatility20"] = df["DailyReturn"].rolling(window=20).std()

# 5) Clean NaNs (from rolling windows)
df_clean = df.dropna().copy()

# -------- Chart 1: Price + Moving Averages --------
plt.figure(figsize=(12, 6))
plt.plot(df_clean.index, df_clean["Close"], label="Close Price")
plt.plot(df_clean.index, df_clean["MA20"], label="20-Day MA")
plt.plot(df_clean.index, df_clean["MA50"], label="50-Day MA")
plt.title(f"{TICKER} Stock Trend: Close Price & Moving Averages (2 Years)")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.tight_layout()
plt.savefig("price_moving_averages.png", dpi=200)
plt.show()

# -------- Chart 2: Rolling Volatility --------
plt.figure(figsize=(12, 6))
plt.plot(df_clean.index, df_clean["Volatility20"], label="20-Day Rolling Volatility")
plt.title(f"{TICKER} Rolling Volatility (20-Day)")
plt.xlabel("Date")
plt.ylabel("Volatility (Std Dev of Daily Returns)")
plt.legend()
plt.tight_layout()
plt.savefig("rolling_volatility.png", dpi=200)
plt.show()

# 6) Quick summary (optional, nice for README)
latest = df_clean.iloc[-1]
print("\n--- Latest Snapshot ---")
print(f"Ticker: {TICKER}")
print(f"Latest Close: {latest['Close']:.2f}")
print(f"MA20: {latest['MA20']:.2f}")
print(f"MA50: {latest['MA50']:.2f}")
print(f"Volatility20: {latest['Volatility20']:.4f}")

print("\nSaved images:")
print(" - price_moving_averages.png")
print(" - rolling_volatility.png")
