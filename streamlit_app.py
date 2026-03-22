import streamlit as st
import telebot
import requests
import threading

# --- ڕێکخستنا لاپەڕێ سایتێ سداد ---
st.set_page_config(page_title="Sidad AI Badini Pro", page_icon="🤖")
st.title("🤖 Sidad AI Dashboard")

# --- وەرگرتنا کلیلان ژ Secrets ---
if "CHATANYWHERE_API_KEY" in st.secrets and "TELEGRAM_BOT_TOKEN" in st.secrets:
    AI_KEY = st.secrets["CHATANYWHERE_API_KEY"]
    BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
    AI_URL = "https://api.chatanywhere.tech/v1/chat/completions"

    bot = telebot.TeleBot(BOT_TOKEN)

    # --- ڕێنماییا بادینی ---
    BADINI_PROMPT = "تو یاریدەدەرەکێ ژیری، تەنێ ب کوردییا بادینی بەرسڤێ بدە."

    def get_ai_response(user_text):
        headers = {"Authorization": f"Bearer {AI_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": BADINI_PROMPT},
                {"role": "user", "content": user_text}
            ]
        }
        try:
            r = requests.post(AI_URL, headers=headers, json=payload)
            return r.json()['choices'][0]['message']['content']
        except:
            return "ئاریشەیەک هەبوو!"

    # --- تێلێگرام بۆت ---
    @bot.message_handler(func=lambda m: True)
    def handle_tg(m):
        reply = get_ai_response(m.text)
        bot.reply_to(m, reply)

    def run_bot():
        bot.remove_webhook()
        bot.polling(none_stop=True)

    if st.button("🚀 دەستپێکرنا بۆتێ تێلێگرامێ"):
        threading.Thread(target=run_bot, daemon=True).start()
        st.success("بۆت چالاک بوو!")

    # --- چاتا ناو سایتی ---
    st.divider()
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("لێرە بنڤیسە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        ans = get_ai_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"):
            st.write(ans)
else:
    st.error("کلیل ل سیکرێتس نینن!")
