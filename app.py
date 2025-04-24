import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import cryptocompare

st.set_page_config(page_title="Scanner MA50", layout="wide")

st.markdown("""
    <style>
        .main { background-color: #f7f9fa; }
        h1, h2, h3 { color: #083759; }
        .st-bw { background-color: white; padding: 1em; border-radius: 10px; box-shadow: 0px 2px 6px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

st.title("Scanner Technique : 🔍 MA50")

@st.cache_data
def get_stock_data(ticker):
    try:
        df = yf.download(ticker.strip(), period="3mo", interval="1d")
        df.dropna(inplace=True)
        return df
    except Exception as e:
        return None

@st.cache_data
def get_crypto_data(symbol):
    try:
        hist = cryptocompare.get_historical_price_day(symbol.strip(), currency='USD', limit=90)
        df = pd.DataFrame(hist)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df.set_index("time", inplace=True)
        df.rename(columns={"close": "Close"}, inplace=True)
        df.dropna(inplace=True)
        return df
    except Exception as e:
        return None

def check_above_ma50(df):
    if "Close" not in df.columns or len(df) < 60:
        return False
    try:
        df["MA50"] = ta.trend.SMAIndicator(close=df["Close"], window=50).sma_indicator()
        return df["Close"].iloc[-1] > df["MA50"].iloc[-1]
    except Exception as e:
        return False

def process_ticker(ticker, is_crypto=False):
    df = get_crypto_data(ticker) if is_crypto else get_stock_data(ticker)
    if df is None:
        return None
    result = {
        "Ticker": ticker,
        "Type": "Crypto" if is_crypto else "Action",
        "Au-dessus MA50": "✅" if check_above_ma50(df) else "❌"
    }
    return result

# 50 principales actions US (exemples)
TOP_50_ACTIONS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "BRK-B", "JPM", "JNJ",
    "V", "PG", "UNH", "HD", "MA", "PFE", "ABBV", "XOM", "BAC", "DIS",
    "KO", "PEP", "ADBE", "CSCO", "NFLX", "WMT", "INTC", "CRM", "T", "VZ",
    "NKE", "ORCL", "MCD", "ABT", "CMCSA", "QCOM", "ACN", "LLY", "TMO", "DHR",
    "AVGO", "COST", "TXN", "NEE", "UPS", "MS", "PM", "HON", "IBM", "UNP"
]

# 50 principales cryptos (symboles)
TOP_50_CRYPTOS = [
    "BTC", "ETH", "BNB", "SOL", "XRP", "ADA", "DOGE", "AVAX", "DOT", "TRX",
    "LINK", "LTC", "MATIC", "XLM", "ATOM", "ETC", "FIL", "APT", "ARB", "IMX",
    "NEAR", "HBAR", "INJ", "ICP", "RNDR", "SUI", "LDO", "EGLD", "GRT", "AAVE",
    "FTM", "KAS", "MKR", "OP", "ALGO", "CHZ", "VET", "STX", "RPL", "DYDX",
    "ZIL", "ENJ", "BCH", "XMR", "CRO", "SAND", "THETA", "AXS", "FLOW", "1INCH"
]

with st.spinner("🔎 Analyse en cours..."):
    results = []

    for ticker in TOP_50_ACTIONS:
        res = process_ticker(ticker.strip(), is_crypto=False)
        if res:
            results.append(res)

    for ticker in TOP_50_CRYPTOS:
        res = process_ticker(ticker.strip(), is_crypto=True)
        if res:
            results.append(res)

if results:
    df_results = pd.DataFrame(results)
    df_actions = df_results[df_results["Type"] == "Action"]
    df_cryptos = df_results[df_results["Type"] == "Crypto"]

    st.subheader("📈 Actions au-dessus de la MA50")
    st.dataframe(df_actions[df_actions["Au-dessus MA50"] == "✅"], use_container_width=True)

    st.subheader("💰 Cryptos au-dessus de la MA50")
    st.dataframe(df_cryptos[df_cryptos["Au-dessus MA50"] == "✅"], use_container_width=True)
else:
    st.warning("Aucun résultat n'a pu être récupéré. Vérifie ta connexion ou réessaie plus tard.")

