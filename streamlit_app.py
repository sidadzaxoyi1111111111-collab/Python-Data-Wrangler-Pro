import streamlit as st
import requests
import telebot
import ccxt
from groq import Groq

# --- 1. ڕێکخستنا کلیلێن نهێنی (Secrets) ---
try:
    # هەمی کلیلێن تە ژ لایێ Streamlit ڤە دهێنە خویندن
    B_KEY = st.secrets["BINANCE_KEY"]
    B_SECRET = st.secrets["BINANCE_SECRET"]
    T_TOKEN = st.secrets["TELEGRAM_TOKEN"]
    T_ID = st.secrets["TELEGRAM_CHAT_ID"]
    G_KEY = st.secrets["GROQ_KEY"]

    # دەسپێکرنا بوتێ تێلێگرام و باینانس
    bot = telebot.TeleBot(T_TOKEN)
    exchange = ccxt.binance({
        'apiKey': B_KEY,
        'secret': B_SECRET,
        'enableRateLimit': True,
        'options': {'defaultType': 'spot'}
    })
    client = Groq(api_key=G_KEY)
except Exception as e:
    st.error(f"❌ Setup Error: {e}. Check your Secrets!")
    st.stop()

# --- 2. فۆنکشنێن بنەڕەتی (Core Functions) ---

def send_alert(msg):
    """فرێکرنا ئاگەهداریێ بۆ تێلێگراما سدادی"""
    try:
        bot.send_message(T_ID, msg)
    except: pass

def get_live_price():
    """خویندنا بهایێ SOL ب شێوەیەکێ لایڤ"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
        return requests.get(url, timeout=10).json()['solana']['usd']
    except:
        return 185.20 # بهایەکێ نێزیکی بازاڕێ ئەڤڕۆ

# --- 3. ڕووکارێ سایتێ سداد (Web Interface) ---

st.set_page_config(page_title="Sidad AI Beast", page_icon="🦾")
st.title("🦾 Sidad AI - $20 Profit Beast")
st.caption("Strategy: Spot Trading | Auto-Buy & Sell | Developed by Sidad")

current_p = get_live_price()
st.metric("Live SOL Price", f"${current_p}")

# نیشاندانا کادرێ پارەی (Account Balance)
try:
    balance = exchange.fetch_balance()
    usdt_balance = balance['total'].get('USDT', 0)
    st.sidebar.metric("Your USDT Balance", f"${usdt_balance:.2f}")
except:
    st.sidebar.warning("Could not fetch Binance balance.")

# --- 4. لۆجیکێ تداولێ (The Trading Brain) ---

st.sidebar.header("📈 Trading Rules")
# ئاستێن کڕین و فرۆتنێ
buy_at = 175.00    # ئەگەر نرخ دابەزی بۆ ڤێرە، بکڕە
tp_level = 210.00  # وەرگرتنا قازانجی (Take Profit)
sl_level = 165.00  # ڕاگرتنا خوسارەتیێ (Stop Loss)

st.sidebar.write(f"Buy Trigger: ${buy_at}")
st.sidebar.success(f"Take Profit: ${tp_level}")
st.sidebar.error(f"Stop Loss: ${sl_level}")

# ١. لۆجیکێ کڕینێ ب $20 دولاران
if usdt_balance >= 10 and current_p <= buy_at:
    st.warning(f"📉 Dip detected! Buying SOL with your $20...")
    try:
        # کڕین ب هەمی کادرێ USDT (وەک ۲۰ دولارێن تە)
        order = exchange.create_market_buy_order('SOL/USDT', usdt_balance)
        send_alert(f"🔥 BUY EXECUTED! Sidad, I used ${usdt_balance} to buy SOL at ${current_p}!")
    except Exception as e: st.error(f"Buy Error: {e}")

# ٢. لۆجیکێ فرۆتنێ (قازانج یان پاراستن)
sol_balance = balance['total'].get('SOL', 0)
if sol_balance > 0:
    if current_p >= tp_level:
        st.balloons()
        try:
            exchange.create_market_sell_order('SOL/USDT', sol_balance)
            send_alert(f"💰 PROFIT TAKEN! Sold SOL at ${current_p}. Great job, Sidad!")
        except Exception as e: st.error(f"Sell Error: {e}")
        
    elif current_p <= sl_level:
        try:
            exchange.create_market_sell_order('SOL/USDT', sol_balance)
            send_alert(f"🛑 STOP LOSS! Sold at ${current_p} to protect your $20, Sidad.")
        except Exception as e: st.error(f"Exit Error: {e}")

# --- 5. چاتا AI یا سدادی ---
st.markdown("---")
if prompt := st.chat_input("Ask the Beast..."):
    with st.chat_message("user"): st.markdown(prompt)
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "You are a crypto trading expert for Sidad."}, {"role": "user", "content": prompt}]
    )
    with st.chat_message("assistant"): st.markdown(resp.choices[0].message.content)
