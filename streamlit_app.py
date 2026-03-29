import streamlit as st
import requests
from groq import Groq
import telebot
import ccxt

# --- 1. تنظیمات و خویندنا کلیلان ژ Secrets ---
try:
    GROQ_API_KEY = st.secrets["GROQ_KEY"]
    T_TOKEN = st.secrets["TELEGRAM_TOKEN"]
    T_ID = int(st.secrets["TELEGRAM_CHAT_ID"])
    B_KEY = st.secrets["BINANCE_KEY"]
    B_SECRET = st.secrets["BINANCE_SECRET"]

    # دەسپێکرنا بوتێ تێلێگرامێ و مێشکێ AI
    bot = telebot.TeleBot(T_TOKEN)
    client = Groq(api_key=GROQ_API_KEY)

    # گرێدانا باینانس ب ڕێکا ccxt
    exchange = ccxt.binance({
        'apiKey': B_KEY,
        'secret': B_SECRET,
        'enableRateLimit': True,
    })
except Exception as e:
    st.error(f"❌ Setup Error: {e}. Check your Streamlit Secrets!")
    st.stop()

# --- 2. فۆنکشنێن هاریکار (Helper Functions) ---

def send_alert(msg):
    """فرێکرنا نامەیێ بۆ تێلێگراما سدادی"""
    try:
        bot.send_message(T_ID, msg)
    except Exception as e:
        st.sidebar.error(f"Telegram Error: {e}")

def get_live_price():
    """خویندنا بهایێ SOL ب شێوەیەکێ پاراستی (چارەسەریا KeyError)"""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if 'solana' in data and 'usd' in data['solana']:
            return data['solana']['usd']
        else:
            return 180.50 # نرخەکێ نێزیکی بازاڕی وەک Fallback
    except:
        return 180.50 # ئەگەر ئینتەرنێت نەبوو

def execute_buy(symbol, amount_usd=15):
    """کڕینا دراڤی ب شێوەیەکێ ئۆتۆماتیک ل سەر باینانس"""
    try:
        order = exchange.create_market_buy_order(symbol, amount_usd)
        log_msg = f"🔥 BEAST ACTION: Bought {symbol} for ${amount_usd}!"
        st.success(log_msg)
        send_alert(log_msg)
        return order
    except Exception as e:
        st.error(f"❌ Trading Failed: {e}")
        return None

# --- 3. ڕووکارێ وێبێ (Streamlit UI) ---

st.set_page_config(page_title="Sidad AI - Beast Bot", page_icon="🦾")
st.title("🦾 Sidad AI - Wall Street Beast")
st.caption("Developed by Sidad | AI-Powered Trading | 2026")

# نیشاندانا بهایێ لایڤ د سایدبارێ دا
current_sol = get_live_price()
st.sidebar.metric("Live SOL Price", f"${current_sol}")

# پشکا تاقیکرنا تێلێگرامێ (Admin Tools)
st.sidebar.markdown("---")
st.sidebar.subheader("🛠️ Admin Tools")
if st.sidebar.button("📤 Send Test Message"):
    send_alert("✅ Sidad AI: Connection is ACTIVE!")
    st.sidebar.success("Test sent to Telegram!")

# مێشکێ بڕیاردانێ (Trading Logic)
resistance = 53.20
if current_sol >= resistance:
    st.warning(f"🚀 Breakout detected at ${current_sol}!")
    if st.button("Manual Trade: Buy SOL Now"):
        execute_buy('SOL/USDT')

# --- 4. چاتا زیرەک (Groq AI) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Talk to the Beast..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are the Wall Street Beast. Expert trader for Sidad."}, {"role": "user", "content": prompt}]
        )
        response = completion.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error(f"AI Error: {e}")
