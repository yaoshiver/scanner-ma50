import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import cryptocompare
from datetime import datetime, timedelta

st.set_page_config(page_title="Scanner MA50 Multi-Timeframe", layout="wide")

st.markdown("""
    <style>
        .main { background-color: #f7f9fa; }
        h1, h2, h3 { color: #083759; }
        .st-bw { background-color: white; padding: 1em; border-radius: 10px; box-shadow: 0px 2px 6px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

st.title("🔍 Scanner MA50 (4H / Daily / Weekly)")

# Définir les tickers
TOP_50_ACTIONS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "BRK-B", "JPM", "JNJ",
    "V", "PG", "UNH", "HD", "MA", "PFE", "ABBV", "XOM", "BAC", "DIS",
    "KO", "PEP", "ADBE", "CSCO", "NFLX", "WMT", "INTC", "CRM", "T", "VZ",
    "NKE", "ORCL", "MCD", "ABT", "CMCSA", "QCOM", "ACN", "LLY", "TMO", "DHR",
    "AVGO", "COST", "TXN", "NEE", "UPS", "MS", "PM", "HON", "IBM", "UNP"
]

TOP_50_CRYPTOS = [
    "BTC", "ETH", "BNB", "SOL", "XRP", "ADA", "DOGE", "AVAX", "DOT", "TRX",
    "LINK", "LTC", "MATIC", "XLM", "ATOM", "ETC", "FIL", "APT", "ARB", "IMX",
    "NEAR", "HBAR", "INJ", "ICP", "RNDR", "SUI", "LDO", "EGLD", "GRT", "AAVE",
    "FTM", "KAS", "MKR", "OP", "ALGO", "CHZ", "VET", "STX", "RPL", "DYDX",
    "ZIL", "ENJ", "BCH", "XMR", "CRO", "SAND", "THETA", "AXS", "FLOW", "1INCH"
]

@st.cache_data
def get_data_yfinance(ticker, period="3mo", interval="1d"):
    try:
        df = yf.download(ticker, period=period, interval=interval, progress=False)
        df.dropna(inplace=True)
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
        df.dropna(inplace=True)
        return df
    except:
        return None

def check_ma50_condition(df):
    if "Close" not in df.columns or len(df) < 60:
        return False
    try:
        df["MA50"] = ta.trend.SMAIndicator(close=df["Close"], window=50).sma_indicator()
        return df["Close"].iloc[-1] > df["MA50"].iloc[-1]
    except:
        return False

def process_ticker_multi_tf(ticker, is_crypto=False):
    timeframes = {
        "4H": ("7d", "1h"),      # environ 4H via 1H interval
        "Daily": ("3mo", "1d"),
        "Weekly": ("2y", "1wk")
    }

    result = {
        "Ticker": ticker,
        "Type": "Crypto" if is_crypto else "Action"
    }

    for tf_label, (period, interval) in timeframes.items():
        if is_crypto and tf_label != "Daily":
            result[tf_label] = "⛔"  # cryptocompare n'offre que le daily
            continue

        df = get_crypto_data(ticker) if is_crypto else get_data_yfinance(ticker, period, interval)
        if df is None:
            result[tf_label] = "❌"
        else:
            result[tf_label] = "✅" if check_ma50_condition(df) else "❌"

    return result

with st.spinner("🔄 Chargement des données..."):
    results = []

    for ticker in TOP_50_ACTIONS:
        results.append(process_ticker_multi_tf(ticker, is_crypto=False))

    for ticker in TOP_50_CRYPTOS:
        results.append(process_ticker_multi_tf(ticker, is_crypto=True))

df_results = pd.DataFrame(results)

# Affichage
st.subheader("📈 Résultats - Actions")
st.dataframe(df_results[df_results["Type"] == "Action"], use_container_width=True)

st.subheader("💰 Résultats - Cryptos")
st.dataframe(df_results[df_results["Type"] == "Crypto"], use_container_width=True)



