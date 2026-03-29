import streamlit as st
from binance.client import Client
from groq import Groq
import pandas as pd

# 1. ڕێکخستنا لاپەرەی
st.set_page_config(page_title="Sidad AI - Wall Street Beast", layout="wide")

# 2. بارکرنا کلیلان ژ Secrets ب پاراستی
try:
    BINANCE_KEY = st.secrets["BINANCE_API_KEY"]
    BINANCE_SECRET = st.secrets["BINANCE_API_SECRET"]
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    
    # دروستکرنا کلاینتێن بینانس و گڕۆق
    client = Client(BINANCE_KEY, BINANCE_SECRET)
    groq_client = Groq(api_key=GROQ_KEY)
    st.sidebar.success("✅ Connected to Binance & Groq")
except Exception as e:
    st.sidebar.error("❌ Configuration Missing! Add Keys to Streamlit Secrets.")
    st.sidebar.info("Please add BINANCE_API_KEY, BINANCE_API_SECRET, and GROQ_API_KEY to your Secrets.")
    st.stop()

# --- سەرناڤێ پڕۆژەی ---
st.title("🤖 Sidad AI - Wall Street Beast")
st.caption(f"Developed by Sidad Ahmad Mohammed | Zakho, Iraq")
st.markdown("---")

# 3. نیشاندانا بالانسێ (Account Balance)
try:
    account = client.get_account()
    balances = [d for d in account['balances'] if float(d['free']) > 0]
    st.subheader("💰 Your Wallet Balance")
    st.table(pd.DataFrame(balances))
except Exception as e:
    st.warning("Could not fetch balance. Check your API permissions.")

st.markdown("---")

# 4. پشکا حیسابکەرا بازاری (Trade Calculator)
st.subheader("📊 Trade Profit/Loss Calculator")
col1, col2, col3 = st.columns(3)
with col1:
    buy_p = st.number_input("Buy Price (USD)", min_value=0.0, step=0.01, value=0.0)
with col2:
    curr_p = st.number_input("Current Price (USD)", min_value=0.0, step=0.01, value=0.0)
with col3:
    qty = st.number_input("Quantity of Coins", min_value=0.0, step=0.0001, value=0.0)

if st.button("CALCULATE PROFIT"):
    if buy_p > 0 and curr_p > 0 and qty > 0:
        investment = buy_p * qty
        current_value = curr_p * qty
        # کێمکرنا پشکا بینانس 0.1%
        net_profit = current_value - investment - (current_value * 0.001)
        profit_pct = (net_profit / investment) * 100
        
        if net_profit > 0:
            st.success(f"🔥 PROFIT: +${net_profit:.2f} ({profit_pct:.2f}%)")
        else:
            st.error(f"📉 LOSS: ${net_profit:.2f} ({profit_pct:.2f}%)")
    else:
        st.info("Please enter all values to calculate.")

st.markdown("---")

# 5. پشکا چاتا زیرەک (Beast AI Chat)
st.subheader("💬 Ask the Beast")
st.info("Ask me about crypto trends or market analysis in English.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("What is the trend for BTC today?"):
    st.session_state.messages.
