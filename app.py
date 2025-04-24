import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import ta
import requests

st.set_page_config(page_title="Scanner LuxAlgo-like", layout="wide")

st.markdown("""
    <style>
        .main { background-color: #f7f9fa; }
        h1, h2, h3 { color: #083759; }
        .st-bw { background-color: white; padding: 1em; border-radius: 10px; box-shadow: 0px 2px 6px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

st.title("Scanner Signal Acheteur/Vendeur (Style LuxAlgo)")

# Top 50 tickers (à titre d'exemple, liste partielle)
top_50_stocks = ["AAPL", "MSFT", "GOOGL", "NVDA", "AMZN", "TSLA", "META", "BRK-B", "UNH", "JNJ"]
top_50_cryptos = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD", "ADA-USD", "AVAX-USD", "DOGE-USD", "DOT-USD", "LINK-USD"]

def get_data(ticker):
    try:
        df = yf.download(ticker, period="3mo", interval="1d")
        df.dropna(inplace=True)
        return df
    except:
        return None

def get_signal(df):
    if len(df) < 60 or "Close" not in df.columns:
        return "Données insuffisantes"

    df["EMA_fast"] = ta.trend.ema_indicator(df["Close"], window=9)
    df["EMA_slow"] = ta.trend.ema_indicator(df["Close"], window=21)
    df["MACD"] = ta.trend.macd(df["Close"])
    df["Signal"] = ta.trend.macd_signal(df["Close"])

    last_close = df["Close"].iloc[-1]
    last_fast = df["EMA_fast"].iloc[-1]
    last_slow = df["EMA_slow"].iloc[-1]
    macd_now = df["MACD"].iloc[-1]
    macd_prev = df["MACD"].iloc[-2]
    signal_now = df["Signal"].iloc[-1]
    signal_prev = df["Signal"].iloc[-2]

    bullish_cross = macd_prev < signal_prev and macd_now > signal_now
    bearish_cross = macd_prev > signal_prev and macd_now < signal_now

    if last_fast > last_slow and bullish_cross:
        return "🟢 Signal Acheteur"
    elif last_fast < last_slow and bearish_cross:
        return "🔴 Signal Vendeur"
    else:
        return "⚪ Aucun signal"

st.subheader("📈 Actions")
stock_results = []
for ticker in top_50_stocks:
    df = get_data(ticker)
    if df is not None:
        signal = get_signal(df)
        stock_results.append({"Ticker": ticker, "Signal": signal})

st.dataframe(pd.DataFrame(stock_results))

st.subheader("🪙 Cryptos")
crypto_results = []
for ticker in top_50_cryptos:
    df = get_data(ticker)
    if df is not None:
        signal = get_signal(df)
        crypto_results.append({"Crypto": ticker, "Signal": signal})

st.dataframe(pd.DataFrame(crypto_results))






