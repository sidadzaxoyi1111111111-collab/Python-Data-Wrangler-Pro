import streamlit as st
import telebot
from threading import Thread

# --- تنظیمات بوت ---
# تەوکنێ تە یێ نوو لێرە دانایە
BOT_TOKEN = "8753625924:AAFxsjaQWOuxbpF4nC9mlMV4SCwjz7uV6Ks"
bot = telebot.TeleBot(BOT_TOKEN)

# --- دیزاینا سایتێ (Streamlit) ---
st.set_page_config(page_title="Sidad AI Agent", page_icon="🤖")

st.title("🚀 Sidad AI Agent Dashboard")
st.write("---")
st.success("سیداد برا، بۆتێ تە و سایتێ تە نوکە ب سەرکەفتی ل سەر Render کار دکەن!")
st.metric(label="Status", value="Online", delta="24/7 Active")

st.info("ئەڤە سایتێ تە یە، و ل باکگراوەندی ژی بۆتێ تە یێ تلەگرامی یێ کار دکەت.")

# --- فرمانێن بۆتی (Telegram Bot) ---
@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        f"سڵاو {message.from_user.first_name} گیان! 👋\n\n"
        "ئەز بۆتێ تایبەتێ سیداد زاخۆیی مە.\n"
        "نوکە ئەز یێ ل سەر Render کار دکەم و ناڕاوەستم! 🚀"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"تە گۆت: {message.text}")

# --- کارپێکرنا بۆتی ---
def run_bot():
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Error: {e}")

# ئەڤ پارجە کۆدە ناهێلیت بۆت زۆر جار دەستپێ بکەتەوە
if "bot_started" not in st.session_state:
    thread = Thread(target=run_bot)
    thread.daemon = True
    thread.start()
    st.session_state.bot_started = True
