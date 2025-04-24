import streamlit as st
import yfinance as yf
import pandas as pd
from ta.trend import EMAIndicator

st.set_page_config(page_title="Scanner Signal EMA", layout="wide")

st.markdown("""
    <style>
        .main { background-color: #f7f9fa; }
        h1, h2, h3 { color: #083759; }
        .st-bw { background-color: white; padding: 1em; border-radius: 10px; box-shadow: 0px 2px 6px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

st.title("Scanner Technique : Signal EMA façon LuxAlgo")

# Top 50 actions et cryptos populaires (simplifiés ici pour l'exemple)
TOP50_STOCKS = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "AMD", "NFLX", "INTC"]
TOP50_CRYPTOS = ["BTC-USD", "ETH-USD", "BNB-USD", "XRP-USD", "SOL-USD", "ADA-USD", "AVAX-USD", "DOGE-USD", "DOT-USD", "MATIC-USD"]

def get_data(ticker):
    try:
        df = yf.download(ticker, period="3mo", interval="1d")
        df.dropna(inplace=True)
        return df
    except:
        return None

def get_signal(df):
    if df is None or df.empty or "Close" not in df.columns:
        return "⛔"

    df = df.copy()
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df.dropna(subset=["Close"], inplace=True)

    if len(df) < 30:
        return "⛔"

    try:
        ema_fast = EMAIndicator(close=df["Close"], window=9).ema_indicator()
        ema_slow = EMAIndicator(close=df["Close"], window=21).ema_indicator()

        df["EMA_fast"] = ema_fast
        df["EMA_slow"] = ema_slow

        if df["EMA_fast"].isna().sum() > 0 or df["EMA_slow"].isna().sum() > 0:
            return "⛔"

        # Croisement haussier (achat)
        if df["EMA_fast"].iloc[-2] < df["EMA_slow"].iloc[-2] and df["EMA_fast"].iloc[-1] > df["EMA_slow"].iloc[-1]:
            return "🟢 Achat"
        # Croisement baissier (vente)
        elif df["EMA_fast"].iloc[-2] > df["EMA_slow"].iloc[-2] and df["EMA_fast"].iloc[-1] < df["EMA_slow"].iloc[-1]:
            return "🔴 Vente"
        else:
            return "🟡 Neutre"
    except Exception:
        return "❌ Erreur"

def afficher_resultats(tickers, titre_section):
    st.subheader(titre_section)
    resultats = []
    for ticker in tickers:
        df = get_data(ticker)
        signal = get_signal(df)
        resultats.append({"Ticker": ticker, "Signal": signal})

    st.dataframe(pd.DataFrame(resultats))

# Affichage des résultats
with st.spinner("Analyse en cours..."):
    afficher_resultats(TOP50_STOCKS, "Top 50 Actions")
    afficher_resultats(TOP50_CRYPTOS, "Top 50 Cryptos")








