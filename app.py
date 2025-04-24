import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import datetime

st.set_page_config(page_title="Signal LuxAlgo Like", layout="wide")

st.title("🔍 Scanner de Signaux Acheteur/Vendeur (Type LuxAlgo) - Journalier")

# Exemple de Top 50 actions (à remplacer ou automatiser si besoin)
TOP50_STOCKS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B", "UNH", "JNJ",
    "XOM", "V", "PG", "JPM", "MA", "HD", "CVX", "ABBV", "AVGO", "LLY",
    "KO", "PEP", "MRK", "BAC", "COST", "MCD", "TMO", "WMT", "NKE", "DIS",
    "ADBE", "CRM", "CSCO", "ABT", "INTC", "DHR", "WFC", "ACN", "TXN", "VZ",
    "LIN", "NEE", "PM", "QCOM", "BMY", "UPS", "MS", "RTX", "ORCL", "LOW"
]

TOP50_CRYPTOS = [
    "BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOGE-USD", "AVAX-USD", "TRX-USD", "DOT-USD",
    "LINK-USD", "MATIC-USD", "TON-USD", "LTC-USD", "SHIB-USD", "BCH-USD", "NEAR-USD", "ICP-USD", "ATOM-USD", "UNI-USD",
    "XLM-USD", "ETC-USD", "HBAR-USD", "APT-USD", "FIL-USD", "IMX-USD", "ARB-USD", "VET-USD", "OP-USD", "MKR-USD",
    "AAVE-USD", "SAND-USD", "EGLD-USD", "GRT-USD", "AXS-USD", "RUNE-USD", "INJ-USD", "XEC-USD", "STX-USD", "KAVA-USD",
    "ZIL-USD", "ALGO-USD", "ENJ-USD", "CHZ-USD", "CRV-USD", "FTM-USD", "DYDX-USD", "CELO-USD", "FLOW-USD", "1INCH-USD"
]

@st.cache_data
def fetch_data(ticker):
    try:
        df = yf.download(ticker, period="3mo", interval="1d")
        if df.empty or "Close" not in df.columns:
            return None
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
        df.dropna(inplace=True)
        return df
    except Exception as e:
        return None

def get_signal(df):
    try:
        close = df["Close"]
        ema_fast = ta.trend.ema_indicator(close=close, window=9).fillna(0)
        ema_slow = ta.trend.ema_indicator(close=close, window=21).fillna(0)

        df["EMA_fast"] = ema_fast
        df["EMA_slow"] = ema_slow

        if len(df) < 2:
            return "⚠️ Données insuffisantes"

        if df["EMA_fast"].iloc[-2] < df["EMA_slow"].iloc[-2] and df["EMA_fast"].iloc[-1] > df["EMA_slow"].iloc[-1]:
            return "🟢 Signal Acheteur"
        elif df["EMA_fast"].iloc[-2] > df["EMA_slow"].iloc[-2] and df["EMA_fast"].iloc[-1] < df["EMA_slow"].iloc[-1]:
            return "🔴 Signal Vendeur"
        else:
            return "⚪️ Aucun Signal"
    except:
        return "❌ Erreur"

def afficher_signaux(tickers, titre):
    st.subheader(titre)
    resultats = []
    for ticker in tickers:
        df = fetch_data(ticker)
        if df is None:
            signal = "❌ Erreur données"
        else:
            signal = get_signal(df)
        resultats.append({"Ticker": ticker, "Signal": signal})

    df_result = pd.DataFrame(resultats)
    st.dataframe(df_result, use_container_width=True)

# Afficher les résultats
afficher_signaux(TOP50_STOCKS, "📈 Top 50 Actions")
afficher_signaux(TOP50_CRYPTOS, "💰 Top 50 Cryptos")









