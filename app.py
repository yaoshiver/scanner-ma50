import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import datetime

st.set_page_config(page_title="Signal LuxAlgo Like", layout="wide")
st.title("🔍 Scanner de Signaux Acheteur/Vendeur (Type LuxAlgo) - Journalier")

# Top 5 en démo pour tester rapidement
TOP50_STOCKS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]
TOP50_CRYPTOS = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD"]

@st.cache_data
def fetch_data(ticker):
    try:
        df = yf.download(ticker, period="3mo", interval="1d")
        if df.empty:
            return None, "Données vides"
        if "Close" not in df.columns:
            return None, "Colonne 'Close' manquante"
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
        df.dropna(inplace=True)
        if df.empty:
            return None, "Toutes les valeurs sont NaN"
        return df, "OK"
    except Exception as e:
        return None, f"Erreur YFinance : {str(e)}"

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
    except Exception as e:
        return f"❌ Erreur Signal : {str(e)}"

def afficher_signaux(tickers, titre):
    st.subheader(titre)
    resultats = []
    for ticker in tickers:
        df, status = fetch_data(ticker)
        if df is None:
            signal = f"❌ {status}"
        else:
            signal = get_signal(df)
        resultats.append({"Ticker": ticker, "Signal": signal})
    st.dataframe(pd.DataFrame(resultats), use_container_width=True)

# Exécution
afficher_signaux(TOP50_STOCKS, "📈 Top 5 Actions")
afficher_signaux(TOP50_CRYPTOS, "💰 Top 5 Cryptos")










