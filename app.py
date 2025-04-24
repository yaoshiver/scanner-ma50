import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.set_page_config(page_title="Signal Acheteur/Vendeur - Style LuxAlgo", layout="wide")
st.title("Signal Acheteur/Vendeur - Style LuxAlgo (EMA 9/21)")

# Top 50 actions populaires (exemples)
TOP50_STOCKS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B", "UNH", "JNJ",
    "V", "JPM", "PG", "MA", "HD", "XOM", "KO", "PEP", "LLY", "ABBV", "MRK", "AVGO",
    "ORCL", "COST", "CVX", "TMO", "MCD", "ACN", "ABT", "QCOM", "TXN", "ADBE",
    "NEE", "WMT", "DHR", "NKE", "CRM", "UPS", "INTC", "PM", "AMD", "LIN",
    "MS", "UNP", "AMGN", "HON", "BA", "RTX", "LMT", "GS"
]

# Top 50 cryptos (exemples)
TOP50_CRYPTOS = [
    "BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD", "ADA-USD", "AVAX-USD", "DOGE-USD",
    "DOT-USD", "TRX-USD", "LINK-USD", "MATIC-USD", "LTC-USD", "BCH-USD", "XLM-USD", "ATOM-USD",
    "NEAR-USD", "HBAR-USD", "IMX-USD", "ETC-USD", "FIL-USD", "RNDR-USD", "ICP-USD", "INJ-USD",
    "VET-USD", "MKR-USD", "GRT-USD", "SAND-USD", "EGLD-USD", "APE-USD", "AAVE-USD", "KAVA-USD",
    "FLOW-USD", "XTZ-USD", "CHZ-USD", "THETA-USD", "AXS-USD", "ENS-USD", "ZEC-USD", "CAKE-USD",
    "XMR-USD", "FTM-USD", "RUNE-USD", "LDO-USD", "CRV-USD", "1INCH-USD", "DYDX-USD", "COMP-USD",
    "ZIL-USD", "BNT-USD"
]

@st.cache_data(show_spinner=False)
def fetch_data(ticker):
    df = yf.download(ticker, period="3mo", interval="1d")
    if not df.empty and "Close" in df.columns:
        df = df.dropna()
        df = df.copy()
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
        df.dropna(subset=["Close"], inplace=True)
        return df
    return None

def get_signal(df):
    if df is None or len(df) < 22:
        return "N/A"
    try:
        df["EMA_fast"] = ta.trend.ema_indicator(df["Close"], window=9)
        df["EMA_slow"] = ta.trend.ema_indicator(df["Close"], window=21)

        if df["EMA_fast"].isna().sum() > 0 or df["EMA_slow"].isna().sum() > 0:
            return "N/A"

        fast_now = df["EMA_fast"].iloc[-1]
        slow_now = df["EMA_slow"].iloc[-1]
        fast_prev = df["EMA_fast"].iloc[-2]
        slow_prev = df["EMA_slow"].iloc[-2]

        if fast_now > slow_now and fast_prev < slow_prev:
            return "Signal Achat ✅"
        elif fast_now < slow_now and fast_prev > slow_prev:
            return "Signal Vente ❌"
        else:
            return "Neutre"
    except:
        return "Erreur"

def afficher_signaux(tickers, label):
    st.subheader(label)
    data = []
    for ticker in tickers:
        df = fetch_data(ticker)
        signal = get_signal(df)
        data.append({"Ticker": ticker, "Signal": signal})
    df_result = pd.DataFrame(data)
    st.dataframe(df_result, use_container_width=True)

# Affichage
col1, col2 = st.columns(2)
with col1:
    afficher_signaux(TOP50_STOCKS, "Top 50 Actions")

with col2:
    afficher_signaux(TOP50_CRYPTOS, "Top 50 Cryptos")








