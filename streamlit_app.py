import streamlit as st
import telebot
import requests
import threading

# --- ڕێکخستنا لاپەڕێ سایتێ سداد ---
st.set_page_config(page_title="Sidad AI Badini Pro", page_icon="🤖")
st.title("🤖 Sidad AI Dashboard")
st.write("سڵاو سداد! ئەڤە پڕۆژەیێ تە یێ تێلێگرامێ و سایتێ تە یە ب زمانی بادینی.")

# --- وەرگرتنا کلیلان ژ Secrets ---
if "CHATANYWHERE_API_KEY" in st.secrets and "TELEGRAM_BOT_TOKEN" in st.secrets:
    AI_KEY = st.secrets["CHATANYWHERE_API_KEY"]
    BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
    AI_URL = "https://api.chatanywhere.tech/v1/chat/completions"

    bot = telebot.TeleBot(BOT_TOKEN)

    # --- سیستەمێ ڕێنماییا بادینی (System Prompt) ---
    BADINI_INSTRUCTIONS = (
        "تو یاریدەدەرەکێ زیرەکی و ناڤێ تە Sidad AI یە. "
        "تەنێ و تەنێ ب زارۆکێ کوردییا بادینی (بەهدینی) بەرسڤێ بدە. "
        "ب چو ڕەنگان ب سۆرانی نەئاخڤە. "
        "ب شوونا 'باشە' بێژە 'گەلەک باشە' یان 'دروستە'. "
        "ب شوونا 'ئێستا' بێژە 'نوکە'. "
        "هەمی بەرسڤێن تە باکوری (بادینی) بن."
    )

    # --- فەنکشنا چاتێ دگەل AI ---
    def get_ai_response(user_text):
        headers = {
            "Authorization": f"Bearer {AI_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": BADINI_INSTRUCTIONS},
                {"role": "user", "content": user_text}
            ],
            "temperature": 0.7
        }
        try:
            response = requests.post(AI_URL, headers=headers, json=payload)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return f"خەتایەک هەبوو ل سێرڤەری: {response.status_code}"
        except Exception as e:
            return f"پەیوەندی دروست نەبوو: {str(e)}"

    # --- پشکا تێلێگرام بۆتی ---
    @bot.message_handler(func=lambda message: True)
    def handle_telegram(message):
        ai_reply = get_ai_response(message.text)
        bot.reply_to(message, ai_reply)

    def run_bot():
        try:
            bot.remove_webhook()
            bot.polling(none_stop=True)
        except:
            pass

    # --- دوگمەیا دەستپێکرنا بۆتی ---
    if st.button("🚀 دەستپێکرنا بۆتێ تێلێگرامێ"):
        # بکارئینانا Threading دا سایت و بۆت پێکڤە کار بکەن
        t = threading.Thread(target=run_bot, daemon=True)
        t.start()
        st.success("✅ بۆت نوکە ل تێلێگرامێ یێ چالاکە! ب بادینی نامەیەکێ بۆ بفرێخە.")

    # --- پشکا چاتا ناو سایتێ Streamlit ---
    st.divider()
    st.subheader("چاتا ناو سایتێ تە:")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(
