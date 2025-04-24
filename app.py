import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import datetime

# Page Configuration
st.set_page_config(page_title="Suivi de Portefeuille Crypto", layout="wide")
st.title("📈 Suivi de Portefeuille Crypto")

# Liste des cryptos dans ton portefeuille
PORTFOLIO = [
    {"crypto": "BTC-USD", "name": "Bitcoin"},
    {"crypto": "ETH-USD", "name": "Ethereum"},
    {"crypto": "BNB-USD", "name": "Binance Coin"},
    {"crypto": "SOL-USD", "name": "Solana"},
    {"crypto": "XRP-USD", "name": "Ripple"},
]

# Initialiser le dataframe qui contiendra le prix initial et les prix quotidiens
@st.cache_data
def get_crypto_data(ticker):
    try:
        # Récupérer les données historiques avec un intervalle de 1 jour
        df = yf.download(ticker, period="30d", interval="1d")
        
        # Vérifier si les données sont disponibles
        if df.empty:
            return None, "❌ Aucune donnée pour cette crypto"
        
        # Ajouter la colonne RSI en utilisant ta librairie ta (RSI sur Weekly)
        df["RSI"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
        
        # Retourner les données et le statut
        return df, "OK"
    
    except Exception as e:
        return None, f"❌ Erreur de récupération des données : {str(e)}"

# Fonction pour déterminer le signal d'achat/vente basé sur le RSI
def get_signal(df):
    try:
        rsi_weekly = df["RSI"].iloc[-1]  # RSI du dernier jour disponible
        
        # Si le RSI est supérieur à 70, signal de vente
        if rsi_weekly > 70:
            return "🔴 Vendre"
        else:
            return "🟢 Conserver"
    except Exception as e:
        return f"❌ Erreur calcul RSI : {str(e)}"

# Fonction pour afficher les résultats dans Streamlit
def afficher_portefeuille(portfolio):
    resultats = []

    for item in portfolio:
        ticker = item["crypto"]
        name = item["name"]
        
        # Récupérer les données de la crypto
        df, status = get_crypto_data(ticker)
        
        # Si les données sont disponibles
        if df is None:
            resultats.append({"Nom": name, "Statut": status})
        else:
            # Fixer le prix initial (prix du jour)
            initial_price = df["Close"].iloc[0]
            today_price = df["Close"].iloc[-1]
            
            # Déterminer le signal d'achat/vente
            signal = get_signal(df)
            
            resultats.append({
                "Nom": name,
                "Prix initial": initial_price,
                "Prix actuel": today_price,
                "Signal": signal,
            })
    
    # Affichage sous forme de tableau dans Streamlit
    st.dataframe(pd.DataFrame(resultats), use_container_width=True)

# Exécution de l'affichage des cryptos du portefeuille
afficher_portefeuille(PORTFOLIO)












