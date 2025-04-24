import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import ta
from datetime import datetime, timedelta

st.set_page_config(page_title="Scanner MA50 + MACD", layout="wide")

st.markdown("""
    <style>
        .main { background-color: #f7f9fa; }
        h1, h2, h3 { color: #083759; }
        .st-bw { background-color: white; padding: 1em; border-radius: 10px; box-shadow: 0px 2px 6px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

st.title("Scanner Technique : MA50 + MACD (Multi-timeframe)")

@st.cache_data

def get_stock_data(ticker, interval, period):
    df = yf.download(ticker, interval=interval, period=period)
    df.dropna(inplace=True)
    return df

def check_conditions(df):
    if "Close" not in df.columns or len(df) < 60:
        return False
    
    df["MA50"] = ta.trend.sma_indicator(df["Close"], window=50)
    macd = ta.trend.macd(df["Close"])
    signal = ta.trend.macd_signal(df["Close"])

    if macd.isna().sum() > 0 or signal.isna().sum() > 0:
        return False

    is_above_ma = df["Close"].iloc[-1] > df["MA50"].iloc[-1]
    macd_now, macd_prev = macd.iloc[-1], macd.iloc[-2]
    signal_now, signal_prev = signal.iloc[-1], signal.iloc[-2]

    cross_up = macd_prev < signal_prev and macd_now > signal_now
    is_positive_zone = macd_now > 0 and signal_now > 0

    return is_above_ma and cross_up and is_positive_zone

def scan_tickers(tickers, label):
    results = []
    for ticker in tickers:
        try:
            row = {"Ticker": ticker}
            for tf_label, interval, period in [("4H", "1h", "7d"), ("Daily", "1d", "3mo"), ("Weekly", "1wk", "1y")]:
                df = get_stock_data(ticker, interval=interval, period=period)
                row[tf_label] = "✅" if check_conditions(df) else "❌"
            results.append(row)
        except:
            continue
    return pd.DataFrame(results)

# Listes des 50 premières actions et cryptos populaires
TOP_50_STOCKS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "BRK-B", "JNJ", "V", "PG", "UNH", "JPM", "HD", "MA",
    "XOM", "LLY", "ABBV", "PEP", "AVGO", "CVX", "MRK", "KO", "COST", "MCD", "WMT", "ADBE", "BAC", "PFE", "CRM", "TMO",
    "NFLX", "ACN", "ABT", "TXN", "ORCL", "DHR", "NKE", "CMCSA", "QCOM", "INTC", "LIN", "AMD", "NEE", "MDT", "AMGN",
    "BMY", "HON", "SBUX", "LOW"
]

TOP_50_CRYPTOS = [
    "BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "ADA-USD", "XRP-USD", "DOGE-USD", "AVAX-USD", "DOT-USD", "TRX-USD",
    "LINK-USD", "MATIC-USD", "TON11419-USD", "SHIB-USD", "LTC-USD", "BCH-USD", "ICP-USD", "XLM-USD", "HBAR-USD",
    "FIL-USD", "APT-USD", "ARB-USD", "NEAR-USD", "VET-USD", "INJ-USD", "QNT-USD", "EGLD-USD", "MKR-USD",
    "AAVE-USD", "STX-USD", "SAND-USD", "XTZ-USD", "AXS-USD", "RUNE-USD", "FTM-USD", "LDO-USD", "SNX-USD",
    "ZIL-USD", "ENJ-USD", "CRV-USD", "1INCH-USD", "CHZ-USD", "DYDX-USD", "COMP-USD", "GRT-USD", "FLOW-USD",
    "IMX-USD", "BAT-USD", "OP-USD", "ALGO-USD"
]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 50 Actions : MA50 + MACD")
    stock_results = scan_tickers(TOP_50_STOCKS, "Actions")
    st.dataframe(stock_results, use_container_width=True)

with col2:
    st.subheader("Top 50 Cryptos : MA50 + MACD")
    crypto_results = scan_tickers(TOP_50_CRYPTOS, "Cryptos")
    st.dataframe(crypto_results, use_container_width=True)





