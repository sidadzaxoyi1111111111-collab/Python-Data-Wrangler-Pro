import streamlit as st
import telebot
import requests
import json
from threading import Thread

# --- ١. خواندنا کلیلان ب شێوەیەکێ پاراستی ژ Streamlit Secrets ---
# ئەڤە دێ کلیلان ژ وێ چوارگۆشەیا ڕەش یا تە لێ سەیڤ کرین وەرگریت
try:
    TOKEN = st.secrets["TOKEN"]
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("سداد برا، کلیل د بەشێ Secrets دا نینن! لایێ چەپێ د Settings دا زێدە بکە.")
    st.stop()

bot = telebot.TeleBot(TOKEN)

# --- ٢. دێزاینا سایتێ Streamlit ---
st.set_page_config(page_title="Sidad AI Agent", page_icon="🐲", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stTitle { color: #2e4053; font-family: 'Arial'; }
    </style>
    """, unsafe_allow_html=True)

st.title("🐲 Sidad AI Agent Portal")
st.info("سڵاو سداد برا! ئەڤە سیستەمێ تە یێ ژیرە کو ب هێزا Groq LPU کار دکەت.")

# --- ٣. لۆژیکێ مێشکێ Groq (Requests) ---
def ask_groq(user_query):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system", 
                "content": "ناڤێ تە Sidad AI یە. تو دێ ب زمانێ کوردی (بادینی) بەرسڤا سداد ئۆ ئەحمەدی دەی ب شێوەیەکێ ب هێز."
            },
            {"role": "user", "content": user_query}
        ],
        "temperature": 0.7
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"خەتایەک هەبوو: {str(e)}"

# --- ٤. بەشێ تێلیگرامێ (ل پشت پەردە) ---
@bot.message_handler(func=lambda message: True)
def telegram_reply(message):
    answer = ask_groq(message.text)
    bot.reply_to(message, answer)

def start_bot():
    bot.polling(none_stop=True)

# کارپێکرنا بۆتی د Threadەکێ جودا دا دا سایت نه‌ڕاوه‌ستیت
if "bot_active" not in st.session_state:
    Thread(target=start_bot, daemon=True).start()
    st.session_state.bot_active = True

# --- ٥. چاتا سەر سایتێ Streamlit ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# پیشاندانا نامەیێن کۆن
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# وەرگرتنا نامەیا نوو ژ سایتێ
if prompt := st.chat_input("تشتەکێ بنڤیسە سداد برا..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("یێ دهزریت..."):
            full_response = ask_groq(prompt)
            st.markdown(full_response)
    st.session_state.chat_history.append({"role": "assistant", "content": full_response})
