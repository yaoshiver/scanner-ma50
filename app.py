import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import cryptocompare
from datetime import datetime

st.set_page_config(page_title="Scanner MA50 Multi-Timeframe", layout="wide")

st.title("📊 Scanner MA50 - 4H / Daily / Weekly")

# Top 50 actions
TOP_50_ACTIONS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "BRK-B", "JPM", "JNJ",
    "V", "PG", "UNH", "HD", "MA", "PFE", "ABBV", "XOM", "BAC", "DIS",
    "KO", "PEP", "ADBE", "CSCO", "NFLX", "WMT", "INTC", "CRM", "T", "VZ",
    "NKE", "ORCL", "MCD", "ABT", "CMCSA", "QCOM", "ACN", "LLY", "TMO", "DHR",
    "AVGO", "COST", "TXN", "NEE", "UPS", "MS", "PM", "HON", "IBM", "UNP"
]

# Top 50 cryptos
TOP_50_CRYPTOS = [
    "BTC", "ETH", "BNB", "SOL", "XRP", "ADA", "DOGE", "AVAX", "DOT", "TRX",
    "LINK", "LTC", "MATIC", "XLM", "ATOM", "ETC", "FIL", "APT", "ARB", "IMX",
    "NEAR", "HBAR", "INJ", "ICP", "RNDR", "SUI", "LDO", "EGLD", "GRT", "AAVE",
    "FTM", "KAS", "MKR", "OP", "ALGO", "CHZ", "VET", "STX", "RPL", "DYDX",
    "ZIL", "ENJ", "BCH", "XMR", "CRO", "SAND", "THETA", "AXS", "FLOW", "1INCH"
]

@st.cache_data
def get_yf_data(ticker, period, interval):
    try:
        df = yf.download(ticker, period=period, interval=interval, progress=False)
        df.dropna(inplace=True)
        return df
    except:
        return None

@st.cache_data
def get_crypto_daily(symbol):
    try:
        hist = cryptocompare.get_historical_price_day(symbol, currency='USD', limit=90)
        df = pd.DataFrame(hist)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df.set_index("time", inplace=True)
        df.rename(columns={"close": "Close"}, inplace=True)
        df.dropna(inplace=True)
        return df
    except:
        return None

def is_above_ma50(df):
    try:
        df["MA50"] = ta.trend.SMAIndicator(close=df["Close"], window=50).sma_indicator()
        return df["Close"].iloc[-1] > df["MA50"].iloc[-1]
    except:
        return False

def analyze_ticker_ma50(ticker, is_crypto=False):
    timeframes = {
        "4H": ("7d", "1h"),     # approximatif pour voir MA50 4H (1h * 50)
        "Daily": ("3mo", "1d"),
        "Weekly": ("2y", "1wk")
    }

    result = {
        "Ticker": ticker,
        "Type": "Crypto" if is_crypto else "Action"
    }

    for tf, (period, interval) in timeframes.items():
        if is_crypto and tf != "Daily":
            result[tf] = "⛔"  # Cryptos seulement sur daily
            continue

        df = get_crypto_daily(ticker) if is_crypto else get_yf_data(ticker, period, interval)
        result[tf] = "✅" if df is not None and is_above_ma50(df) else "❌"

    return result

with st.spinner("🔄 Analyse en cours..."):
    results = []

    for ticker in TOP_50_ACTIONS:
        results.append(analyze_ticker_ma50(ticker, is_crypto=False))

    for ticker in TOP_50_CRYPTOS:
        results.append(analyze_ticker_ma50(ticker, is_crypto=True))

df_results = pd.DataFrame(results)

# Affichage
st.subheader("📈 Actions - MA50")
st.dataframe(df_results[df_results["Type"] == "Action"], use_container_width=True)

st.subheader("💰 Cryptos - MA50")
st.dataframe(df_results[df_results["Type"] == "Crypto"], use_container_width=True)




