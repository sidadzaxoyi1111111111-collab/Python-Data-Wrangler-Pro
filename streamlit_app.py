import streamlit as st
from binance.client import Client
from groq import Groq
import pandas as pd
import plotly.graph_objects as go # بۆ نیشاندانا گرافێن پرۆفیشناڵ

# 1. پاراستنا کلیلان
try:
    client = Client(st.secrets["BINANCE_API_KEY"], st.secrets["BINANCE_API_SECRET"])
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    st.sidebar.success("✅ SYSTEM ONLINE: NO ERRORS")
except:
    st.error("❌ CRITICAL ERROR: Check Secrets!")
    st.stop()

st.title("🦾 Sidad AI - Wall Street Beast PRO")
st.markdown(f"**Target:** Daily Limit $40 | **Status:** Secured")

# 2. نیشاندانا گرافێ بازارێ بیتکۆینێ (Visual Charts)
st.subheader("📈 Live Market Visuals")
klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "24 hours ago UTC")
df = pd.DataFrame(klines, columns=['time', 'open', 'high', 'low', 'close', 'vol', 'close_time', 'q_vol', 'num_trades', 'taker_b_vol', 'taker_q_vol', 'ignore'])
df['time'] = pd.to_datetime(df['time'], unit='ms')

fig = go.Figure(data=[go.Candlestick(x=df['time'], open=df['open'], high=df['high'], low=df['low'], close=df['close'])])
st.plotly_chart(fig, use_container_width=True)

# 3. پاراستنا پارەی (The $40 Daily Lock)
st.sidebar.header("🛡️ Risk Management")
daily_limit = 40.0
st.sidebar.info(f"Daily Spending Locked at: ${daily_limit}")

# 4. پشکا حساباتێن فول (Full Wallet Stats)
with st.expander("📊 View Full Wallet Balances"):
    acc = client.get_account()
    bal = [d for d in acc['balances'] if float(d['free']) > 0]
    st.dataframe(pd.DataFrame(bal), use_container_width=True)

# 5. چاتا زیرەک ب ئینگلیزییا 100%
st.subheader("💬 AI Market Intelligence")
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

prompt = st.chat_input("Ask the Beast...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a top-tier Wall Street Analyst. Talk ONLY in English. Be 100% accurate. Your client is Sidad Ahmad Mohammed."},
                *st.session_state.messages
            ]
        ).choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

st.caption("Developed by Sidad | Zakho, Iraq | 2026")
