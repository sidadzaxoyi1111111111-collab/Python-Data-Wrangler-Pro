import streamlit as st
import requests
from groq import Groq
import telebot

# --- 1. خویندنا کلیلان ژ Secrets (Security First) ---
try:
    GROQ_API_KEY = st.secrets["GROQ_KEY"]
    TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
    CHAT_ID = int(st.secrets["TELEGRAM_CHAT_ID"]) # گوهۆڕین بۆ ژمارە
    
    # دەسپێکرنا کلاینتان
    client = Groq(api_key=GROQ_API_KEY)
    bot = telebot.TeleBot(TELEGRAM_TOKEN)
except Exception as e:
    st.error(f"❌ Error loading Secrets: {e}. Please check your Streamlit Secrets settings.")
    st.stop()

# --- 2. فۆنکشنێن پڕۆژەی (Helper Functions) ---

def send_telegram_alert(message):
    """فرێکرنا ئاگەهداریێ بۆ تێلێگراما سدادی"""
    try:
        bot.send_message(CHAT_ID, message)
    except Exception as e:
        st.sidebar.error(f"Telegram Notification Failed: {e}")

def get_live_crypto_price():
    """خویندنا بهایێ دراڤان ژ CoinGecko دا تووشی بلۆکا باینانس نەبی ل زاخۆ"""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=solana,bitcoin&vs_currencies=usd"
    try:
        response = requests.get(url).json()
        return response['solana']['usd']
    except:
        return 82.36 # نرخەکێ نموونە ئەگەر کێشە هەبیت

def run_beast_logic(price):
    """مێشکێ شیکاریێ یێ ئۆتۆماتیک (The Beast Logic)"""
    resistance_level = 53.20
    if price >= resistance_level:
        msg = f"🦾 Sidad AI - Beast Alert!\n🚀 Price hit: ${price}\n✅ Breakout confirmed! GO LONG NOW!"
        st.success(msg)
        st.balloons()
        # فرێکرنا نامەیێ بتنێ ئێک جار (بۆ نموونە)
        if "alert_sent" not in st.session_state:
            send_telegram_alert(msg)
            st.session_state.alert_sent = True

# --- 3. ڕووکارێ وێبێ (Streamlit UI) ---

st.set_page_config(page_title="Sidad AI - Wall Street Beast", page_icon="🦾")
st.title("🦾 Sidad AI - Wall Street Beast")
st.caption("Developed by Sidad | Powered by Groq AI | 2026")

# پشکا لایڤ داتایێ (Sidebar)
current_price = get_live_crypto_price()
st.sidebar.metric("Live SOL Price", f"${current_price}")
run_beast_logic(current_price)

# دوگمەیا تاقیکرنێ (Manual Test)
if st.sidebar.button("Test Telegram Connection"):
    send_telegram_alert("✅ Sidad, your AI Beast is alive and connected!")
    st.sidebar.write("Message Sent!")

# --- 4. چاتا زیرەک (AI Chat System) ---

if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشاندانا نامەیێن جاران
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# وەرگرتنا پرسیارا سدادی
if prompt := st.chat_input("Talk to the Beast..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # شیکاریا AI ب شێوازێ Wall Street
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are the Wall Street Beast. Expert in crypto. Talk to your creator Sidad. Be bold and professional."},
                {"role": "user", "content": prompt}
            ]
        )
        response = completion.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error(f"AI Connection Error: {e}")
