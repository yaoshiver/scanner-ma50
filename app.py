import streamlit as st
import yfinance as yf
import pandas as pd
import ta
from ta.trend import EMAIndicator

# ------------------------------
# Configuration de l'app
# ------------------------------
st.set_page_config(page_title="Scanner Acheteur/Vendeur", layout="wide")

st.markdown("""
    <style>
        .main { background-color: #f7f9fa; }
        h1, h2, h3 { color: #083759; }
        .st-bw { background-color: white; padding: 1em; border-radius: 10px; box-shadow: 0px 2px 6px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

st.title("Scanner LuxAlgo-Like : Signaux Acheteur/Vendeur (Daily)")

# ------------------------------
# Listes TOP 50 actions & cryptos (à adapter dynamiquement si besoin)
# ------------------------------
TOP50_STOCKS = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "TSLA", "META", "BRK-B", "LLY", "JPM"]  # raccourci ici
TOP50_CRYPTOS = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD", "DOGE-USD", "ADA-USD", "AVAX-USD", "DOT-USD", "LINK-USD"]

# ------------------------------
# Fonction de téléchargement des données
# ------------------------------
def get_data(ticker):
    try:
        df = yf.download(ticker, period="3mo", interval="1d")
        df.dropna(inplace=True)
        return df
    except:
        return None

# ------------------------------
# Fonction de signal type LuxAlgo (cross EMA 9 / 21)
# ------------------------------
def get_signal(df):
    close = df["Close"].astype(float)
    ema_fast = EMAIndicator(close=close, window=9).ema_indicator()
    ema_slow = EMAIndicator(close=close, window=21).ema_indicator()

    df["EMA_fast"] = ema_fast
    df["EMA_slow"] = ema_slow

    if len(df) < 2 or df["EMA_fast"].isna().sum() > 0 or df["EMA_slow"].isna().sum() > 0:
        return "❓ Données insuffisantes"

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

# ------------------------------
# Affichage des résultats
# ------------------------------

def afficher_resultats(tickers, label):
    st.subheader(label)
    results = []
    for ticker in tickers:
        df = get_data(ticker)
        if df is not None:
            signal = get_signal(df)
            results.append({"Ticker": ticker, "Signal": signal})

    df_results = pd.DataFrame(results)
    st.dataframe(df_results, use_container_width=True)

# ------------------------------
# Lancement
# ------------------------------
col1, col2 = st.columns(2)

with col1:
    afficher_resultats(TOP50_STOCKS, "Top 50 Actions")

with col2:
    afficher_resultats(TOP50_CRYPTOS, "Top 50 Cryptos")








