import streamlit as st
import telebot
import requests
import threading

# ڕێکخستنا لاپەڕێ سایتێ تە
st.set_page_config(page_title="Sidad AI Pro", page_icon="🤖")
st.title("🤖 Sidad AI Dashboard")

# وەرگرتنا کلیلان ژ Secrets (پێدڤییە ل ستریملێت دابنێی)
if "CHATANYWHERE_API_KEY" in st.secrets and "TELEGRAM_BOT_TOKEN" in st.secrets:
    AI_KEY = st.secrets["CHATANYWHERE_API_KEY"]
    BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
    AI_URL = "https://api.chatanywhere.tech/v1/chat/completions"

    bot = telebot.TeleBot(BOT_TOKEN)

    # --- پشکا تێلێگرام بۆتی ---
    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        headers = {"Authorization": f"Bearer {AI_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "تو یاریدەدەرەکێ ژیری ب زمانی کوردی بادینی بەرسڤێ ددەی."},
                {"role": "user", "content": message.text}
            ]
        }
        try:
            response = requests.post(AI_URL, headers=headers, json=payload)
            ai_reply = response.json()['choices'][0]['message']['content']
            bot.reply_to(message, ai_reply)
        except:
            bot.reply_to(message, "ببورە سداد، سێرڤەر مژوولە!")

    # فەنکشن بۆ دەستپێکرنا بۆتی د باکگراوندێ دا
    def run_bot():
        bot.remove_webhook()
        bot.polling(none_stop=True)

    st.success("✅ کلیل یێن گرێدای!")
    
    if st.button("🚀 دەستپێکرنا بۆتێ تێلێگرامێ"):
        # بکارئینانا Threading دا کو سایت و بۆت پێکڤە کار بکەن
        threading.Thread(target=run_bot, daemon=True).start()
        st.info("بۆت نوکە یێ کار دکەت! بچۆ تێلێگرامێ و تاقی بکە.")

    # --- پشکا سایتێ تە (وەک بەری نوکە) ---
    st.divider()
    st.subheader("چات لێرە ژی بکە:")
    user_input = st.text_input("نامەیا خۆ لێرە بنڤیسە:")
    if user_input:
        headers = {"Authorization": f"Bearer {AI_KEY}", "Content-Type": "application/json"}
        data = {"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": user_input}]}
        res = requests.post(AI_URL, headers=headers, json=data)
        st.write(res.json()['choices'][0]['message']['content'])

else:
    st.error("تکایە بڕۆ Settings > Secrets و 'TELEGRAM_BOT_TOKEN' زێدە بکە.")
