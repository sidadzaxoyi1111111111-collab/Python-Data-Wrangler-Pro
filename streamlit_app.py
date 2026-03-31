import streamlit as st
import telebot
import requests
import json
from threading import Thread

# --- ١. وەرگرتنا کلیلان ژ Secrets ب شێوەیەکێ پاراستی ---
try:
    TOKEN = st.secrets["TOKEN"]
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("سداد برا، کلیل د بەشێ Secrets دا نینن! لایێ چەپێ د Settings دا زێدە بکە.")
    st.stop()

bot = telebot.TeleBot(TOKEN)

# --- ٢. دێزاینا سایتێ Streamlit ---
st.set_page_config(page_title="Sidad AI Agent", page_icon="🐲", layout="centered")

st.title("🐲 Sidad AI Agent Portal")
st.markdown("---")
st.info("سڵاو سداد برا! ئەڤە سیستەمێ تە یێ ژیرە کو ب مێشکێ Llama 3.3 کار دکەت.")

# --- ٣. لۆژیکێ مێشکێ Groq دگەل نووترین مۆدێل ---
def ask_groq(user_query):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # بکارئینانا مۆدێلێ نوو یێ Groq
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system", 
                "content": "ناڤێ تە Sidad AI یە. تو خزمەتکارێ سداد ئۆ ئەحمەدی و دێ تەنێ ب زمانێ کوردی (تایبەت بادینی) بەرسڤێ دەی."
            },
            {"role": "user", "content": user_query}
        ],
        "temperature": 0.6
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        res_json = response.json()
        
        if 'choices' in res_json:
            return res_json['choices'][0]['message']['content']
        else:
            error_msg = res_json.get('error', {}).get('message', 'خەتایەکا نەدیار د گروق دا')
            return f"⚠️ خەتایا Groq: {error_msg}"
            
    except Exception as e:
        return f"❌ کێشە د پەیوەندیێ دا: {str(e)}"

# --- ٤. بەشێ تێلیگرامێ (Background Thread) ---
@bot.message_handler(func=lambda message: True)
def telegram_reply(message):
    answer = ask_groq(message.text)
    bot.reply_to(message, answer)

def start_bot():
    try:
        bot.polling(none_stop=True)
    except:
        pass

# کارپێکرنا بۆتی دا کو سایت نه‌ڕاوه‌ستیت
if "bot_active" not in st.session_state:
    Thread(target=start_bot, daemon=True).start()
    st.session_state.bot_active = True

# --- ٥. چاتا سەر سایتێ Streamlit ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# پیشاندانا نامەیان
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# وەرگرتنا نامەیا نوو
if prompt := st.chat_input("تشتەکێ بنڤیسە سداد برا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("یێ دهزریت..."):
            response = ask_groq(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
