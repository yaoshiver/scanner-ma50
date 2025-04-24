import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import datetime

# Page Configuration
st.set_page_config(page_title="Signal LuxAlgo Like", layout="wide")
st.title("🔍 Scanner de Signaux Acheteur/Vendeur (Type LuxAlgo) - Journalier")

# Top 5 en démo pour tester rapidement
TOP50_STOCKS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]
TOP50_CRYPTOS = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD"]

@st.cache_data
def fetch_data(ticker):
    try:
        # Récupération des données sur 3 mois avec intervalle de 1 jour
        df = yf.download(ticker, period="3mo", interval="1d")
        
        # Affichage des 5 premières lignes pour voir les données
        if df.empty:
            return None, f"❌ Aucune donnée disponible pour {ticker}"
        
        st.write(f"📊 Données de {ticker} :")
        st.write(df.head())  # Afficher les 5 premières lignes pour vérifier les données

        # Vérification si la colonne 'Close' existe
        if "Close" not in df.columns:
            return None, "Colonne 'Close' manquante dans les données"
        
        # Conversion des données 'Close' en numérique
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
        df.dropna(inplace=True)  # Suppression des valeurs NaN

        # Vérifier si les données sont encore présentes après nettoyage
        if df.empty:
            return None, "Toutes les valeurs sont NaN après nettoyage"
        
        return df, "OK"
    
    except Exception as e:
        return None, f"❌ Erreur lors de la récupération des données : {str(e)}"

def get_signal(df):
    try:
        close = df["Close"]
        
        # Calcul des indicateurs EMA
        ema_fast = ta.trend.ema_indicator(close=close, window=9)
        ema_slow = ta.trend.ema_indicator(close=close, window=21)
        
        df["EMA_fast"] = ema_fast
        df["EMA_slow"] = ema_slow
        
        # Assurer qu'il y a au moins deux points pour le croisement
        if len(df) < 2:
            return "⚠️ Données insuffisantes"

        # Détection du croisement EMA
        if df["EMA_fast"].iloc[-2] < df["EMA_slow"].iloc[-2] and df["EMA_fast"].iloc[-1] > df["EMA_slow"].iloc[-1]:
            return "🟢 Signal Acheteur"
        elif df["EMA_fast"].iloc[-2] > df["EMA_slow"].iloc[-2] and df["EMA_fast"].iloc[-1] < df["EMA_slow"].iloc[-1]:
            return "🔴 Signal Vendeur"
        else:
            return "⚪️ Aucun Signal"
    
    except Exception as e:
        return f"❌ Erreur calcul du signal : {str(e)}"

def afficher_signaux(tickers, titre):
    st.subheader(titre)
    resultats = []
    
    for ticker in tickers:
        # Récupérer les données
        df, status = fetch_data(ticker)
        
        # Si les données sont disponibles, on calcule le signal
        if df is None:
            signal = f"❌ {status}"
        else:
            signal = get_signal(df)
        
        resultats.append({"Ticker": ticker, "Signal": signal})
    
    # Affichage des résultats sous forme de tableau
    st.dataframe(pd.DataFrame(resultats), use_container_width=True)

# Exécution des affichages pour les actions et les cryptos
afficher_signaux(TOP50_STOCKS, "📈 Top 5 Actions")
afficher_signaux(TOP50_CRYPTOS, "💰 Top 5 Cryptos")











