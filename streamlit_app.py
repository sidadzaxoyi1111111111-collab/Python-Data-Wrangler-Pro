import streamlit as st
import requests
import telebot
import ccxt
from groq import Groq

# --- 1. خویندنا کلیلان و تنظیمات ---
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

# --- 2. فۆنکشنێن ئاگەهداری و بازار (Core Functions) ---

def send_alert(msg):
    """فرێکرنا نامەیێ بۆ تێلێگراما سدادی"""
    try:
        bot.send_message(T_ID, msg)
    except: pass

def get_price():
    """خویندنا بهایێ SOL ب شێوەیەکێ پاراستی"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
        return requests.get(url, timeout=10).json()['solana']['usd']
    except: return 180.50

# --- 3. لۆجیکێ تداولێ یێ زیرەک (Smart Trading) ---

st.set_page_config(page_title="Sidad AI Beast", page_icon="🦾")
st.title("🦾 Sidad AI - The Ultimate Profit Beast")
st.caption("Strategy: Automatic Profit Taking & Stop Loss | Developed by Sidad")

current_p = get_price()
st.metric("Live SOL Price", f"${current_p}")

# دیارکرنا ئاستێن قازانج و خوسارەتیێ
st.sidebar.header("📈 Strategy Settings")
entry_p = 150.00 # بهایێ تە پێ کڕی
tp_level = 210.00 # ئارمانجا قازانجی (Take Profit)
sl_level = 140.00 # ڕاگرتنا خوسارەتیێ (Stop Loss)

st.sidebar.write(f"Entry: ${entry_p}")
st.sidebar.success(f"Take Profit: ${tp_level}")
st.sidebar.error(f"Stop Loss: ${sl_level}")

# --- 4. جێبەجێکرنا بڕیارێن ئۆتۆماتیک ---

# ئایا کاتێ قازانجێ یە؟
if current_p >= tp_level:
    st.balloons()
    try:
        # فرۆتنا هەمی SOL یان بۆ وەرگرتنا قازانجی
        exchange.create_market_sell_order('SOL/USDT', 0.1) 
        send_alert(f"💰 PROFIT SECURED! Sold SOL at ${current_p}. Sidad, you won this trade!")
        st.success("Target Hit! Profit Taken.")
    except Exception as e: st.error(f"Sell Error: {e}")

# ئایا بازاڕ یێ مەترسیدارە؟ (Stop Loss)
elif current_p <= sl_level:
    try:
        # فرۆتن بۆ ڕاگرتنا خوسارەتیێ
        exchange.create_market_sell_order('SOL/USDT', 0.1)
        send_alert(f"🛑 STOP LOSS TRIGGERED! Sold at ${current_p} to protect your capital, Sidad.")
        st.warning("Stop Loss Hit. Capital Protected.")
    except Exception as e: st.error(f"Exit Error: {e}")

# --- 5. چاتا AI بۆ شیرەتێن بازاڕی ---
st.markdown("---")
if prompt := st.chat_input("Ask the Beast about market trends..."):
    with st.chat_message("user"): st.markdown(prompt)
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "You are a professional trader focused on profit for Sidad."}, {"role": "user", "content": prompt}]
    )
    with st.chat_message("assistant"): st.markdown(resp.choices[0].message.content)
