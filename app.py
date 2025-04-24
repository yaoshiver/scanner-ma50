import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import cryptocompare

st.set_page_config(page_title="Scanner Signal Acheteur/Vendeur", layout="wide")

st.title("📊 Scanner LuxAlgo Style - Top 50 Actions & Cryptos (Journalier)")

# === FONCTIONS ===
@st.cache_data
def get_stock_data(ticker):
    try:
        df = yf.download(ticker, period="3mo", interval="1d")
        df = df[["Close"]].dropna()
        return df
    except:
        return None

@st.cache_data
def get_crypto_data(symbol):
    try:
        hist = cryptocompare.get_historical_price_day(symbol, currency='USD', limit=90)
        df = pd.DataFrame(hist)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df.set_index("time", inplace=True)
        df.rename(columns={"close": "Close"}, inplace=True)
        df = df[["Close"]].dropna()
        return df
    except:
        return None

def get_signal(df):
    df["EMA_fast"] = ta.trend.ema_indicator(df["Close"].astype(float), window=9)
    df["EMA_slow"] = ta.trend.ema_indicator(df["Close"].astype(float), window=21)

    last_fast = df["EMA_fast"].iloc[-1]
    last_slow = df["EMA_slow"].iloc[-1]
    prev_fast = df["EMA_fast"].iloc[-2]
    prev_slow = df["EMA_slow"].iloc[-2]

    if prev_fast < prev_slow and last_fast > last_slow:
        return "🟢 Signal Acheteur"
    elif prev_fast > prev_slow and last_fast < last_slow:
        return "🔴 Signal Vendeur"
    else:
        return "⚪️ Neutre"

# === TICKERS ===
TOP_50_ACTIONS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "BRK-B", "JNJ", "JPM",
    "V", "UNH", "MA", "PG", "HD", "XOM", "PFE", "BAC", "VZ", "ADBE",
    "KO", "NFLX", "T", "WMT", "PEP", "MRK", "CRM", "CSCO", "ABT", "TMO",
    "NKE", "CVX", "ORCL", "ACN", "AVGO", "MCD", "LLY", "AMD", "INTC", "LIN",
    "QCOM", "UPS", "COST", "PM", "TXN", "HON", "MS", "GS", "BLK", "BMY"
]

TOP_50_CRYPTOS = [
    "BTC", "ETH", "BNB", "SOL", "XRP", "DOGE", "ADA", "AVAX", "DOT", "TRX",
    "LINK", "MATIC", "TON", "UNI", "BCH", "XLM", "LTC", "APT", "INJ", "NEAR",
    "ARB", "ETC", "FIL", "HBAR", "ICP", "VET", "EGLD", "FTM", "RUNE", "MKR",
    "AAVE", "SAND", "AXS", "FLOW", "THETA", "ZIL", "GRT", "CRV", "KAVA", "ENJ",
    "BAT", "XEC", "1INCH", "COMP", "DYDX", "IMX", "LDO", "WOO", "YFI", "ZRX"
]

# === ANALYSE ===
st.subheader("🔍 Résultats des signaux journaliers")

results = []

for ticker in TOP_50_ACTIONS:
    df = get_stock_data(ticker)
    if df is not None and len(df) > 30:
        signal = get_signal(df)
        results.append({"Nom": ticker, "Catégorie": "Action", "Signal": signal})

for crypto in TOP_50_CRYPTOS:
    df = get_crypto_data(crypto)
    if df is not None and len(df) > 30:
        signal = get_signal(df)
        results.append({"Nom": crypto, "Catégorie": "Crypto", "Signal": signal})

df_result = pd.DataFrame(results)
df_result = df_result.sort_values(by="Signal", ascending=False)

st.dataframe(df_result, use_container_width=True)






