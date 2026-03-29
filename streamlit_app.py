import streamlit as st
import requests
import telebot
import ccxt
from groq import Groq

# --- 1. ڕێکخستنا کلیلان (Secrets) ---
try:
    B_KEY = st.secrets["BINANCE_KEY"]
    B_SECRET = st.secrets["BINANCE_SECRET"]
    T_TOKEN = st.secrets["TELEGRAM_TOKEN"]
    T_ID = st.secrets["TELEGRAM_CHAT_ID"]
    G_KEY = st.secrets["GROQ_KEY"]

    bot = telebot.TeleBot(T_TOKEN)
    exchange = ccxt.binance({
        'apiKey': B_KEY,
        'secret': B_SECRET,
        'enableRateLimit': True,
        'options': {'defaultType': 'spot'}
    })
    client = Groq(api_key=G_KEY)
except Exception as e:
    st.error(f"❌ Configuration Error: {e}")
    st.stop()

# --- 2. فۆنکشنێن بنەڕەتی ---

def send_alert(msg):
    try:
        bot.send_message(T_ID, msg)
    except: pass

def get_live_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
        return requests.get(url, timeout=10).json()['solana']['usd']
    except:
        return 185.50 # بهایەکێ نێزیک ئەگەر API کار نەکر

# --- 3. ڕووکارێ سایتێ سداد (UI) ---

st.set_page_config(page_title="Sidad AI Beast", page_icon="🦾")
st.title("🦾 Sidad AI - $20 Profit Beast")
st.caption("Strategy: Spot Trading | Auto-Buy & Sell | Developed by Sidad")

current_p = get_live_price()
st.metric("Live SOL Price", f"${current_p}")

# دانانا بهایێن سەرەتایی دا NameError چێ نەبیت
usdt_balance = 0.0
sol_balance = 0.0

try:
    balance = exchange.fetch_balance()
    usdt_balance = balance['total'].get('USDT', 0)
    sol_balance = balance['total'].get('SOL', 0)
    st.sidebar.metric("Your USDT Balance", f"${usdt_balance:.2f}")
    st.sidebar.metric("Your SOL Balance", f"{sol_balance:.4f}")
except:
    st.sidebar.warning("⚠️ Binance: Waiting for connection...")

# --- 4. لۆجیکێ تداولێ (The Brain) ---

st.sidebar.header("📈 Trading Rules")
buy_at = 175.00
tp_level = 210.00
sl_level = 165.00

st.sidebar.write(f"Buy Trigger: ${buy_at}")
st.sidebar.success(f"Take Profit: ${tp_level}")
st.sidebar.error(f"Stop Loss: ${sl_level}")

# لۆجیکێ کڕینێ ب ئەو $20 یێن تە
if usdt_balance >= 10 and current_p <= buy_at:
    st.warning(f"📉 Signal: Buying SOL with ${usdt_balance}...")
    try:
        order = exchange.create_market_buy_order('SOL/USDT', usdt_balance)
        send_alert(f"🔥 BUY EXECUTED! Sidad, I used ${usdt_balance} to buy SOL at ${current_p}!")
    except Exception as e: st.error(f"Buy Error: {e}")

# لۆجیکێ فرۆتنێ (قازانج یان پاراستن)
if sol_balance > 0:
    if current_p >= tp_level:
        st.balloons()
        try:
            exchange.create_market_sell_order('SOL/USDT', sol_balance)
            send_alert(f"💰 PROFIT TAKEN! Sold SOL at ${current_p}. Well done, Sidad!")
        except Exception as e: st.error(f"Sell Error: {e}")
        
    elif current_p <= sl_level:
        try:
            exchange.create_market_sell_order('SOL/USDT', sol_balance)
            send_alert(f"🛑 STOP LOSS! Sold at ${current_p} to protect your capital, Sidad.")
        except Exception as e: st.error(f"Exit Error: {e}")

# --- 5. چاتا AI یا سداد ---
st.markdown("---")
if prompt := st.chat_input("Ask the Beast..."):
    with st.chat_message("user"): st.markdown(prompt)
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "You are a professional crypto trader for Sidad."}, {"role": "user", "content": prompt}]
    )
    with st.chat_message("assistant"): st.markdown(resp.choices[0].message.content)
