import streamlit as st
from binance.client import Client
from groq import Groq
import pandas as pd
import plotly.graph_objects as go

# پشکنینا کلیلان ب ناڤێن سادە
try:
    # ل ڤێرێ مە ناڤ کورت کرن دا خەلەتی چێ نەبیت
    BINANCE_KEY = st.secrets["BINANCE_KEY"]
    BINANCE_SECRET = st.secrets["BINANCE_SECRET"]
    GROQ_KEY = st.secrets["GROQ_KEY"]
    
    client = Client(BINANCE_KEY, BINANCE_SECRET)
    groq_client = Groq(api_key=GROQ_KEY)
    st.sidebar.success("✅ SYSTEM ONLINE: NO ERRORS")
except Exception as e:
    st.sidebar.error(f"❌ ERROR: {e}")
    st.error("Please check your Secrets names on Streamlit.")
    st.stop()

st.title("🦾 Sidad AI - Wall Street Beast PRO")
st.markdown("**Status:** Secured & Connected")

# --- پشکا گرافان ---
try:
    klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "24 hours ago UTC")
    df = pd.DataFrame(klines, columns=['time', 'open', 'high', 'low', 'close', 'vol', 'close_time', 'q_vol', 'num_trades', 'taker_b_vol', 'taker_q_vol', 'ignore'])
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    fig = go.Figure(data=[go.Candlestick(x=df['time'], open=df['open'], high=df['high'], low=df['low'], close=df['close'])])
    st.plotly_chart(fig, use_container_width=True)
except:
    st.warning("Could not load charts. Check API permissions.")

# --- پشکا چاتا ئینگلیزی ---
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
            messages=[{"role": "system", "content": "You are a Wall Street Analyst. Talk ONLY in English to Sidad Ahmad Mohammed."}, *st.session_state.messages]
        ).choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

st.caption("Developed by Sidad | Zakho, Iraq | 2026")
