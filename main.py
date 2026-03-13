import streamlit as st
import telebot
from threading import Thread

# 1. تەوکنێ تە یێ نوو لێرە دانایە
BOT_TOKEN = "8753625924:AAFxsjaQWOuxbpF4nC9mlMV4SCwjz7uV6Ks"
bot = telebot.TeleBot(BOT_TOKEN)

# دیزاینا سایتێ تە
st.title("🤖 Sidad AI Agent")
st.success("سیداد برا، بوت و سایتێ تە نوکە یێ کار دکەن!")
st.metric(label="Status", value="Online", delta="24/7 Active")

# فرمانێن بوتێ تلەگرامی
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "سڵاو سیداد! ئەز بوتێ تە مە و ل سەر Render یێ کارا مە. 🚀")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"تە گۆت: {message.text}")

# کارپێکرنا بوتێ د باکگراوەندی دا
def run_bot():
    bot.polling(none_stop=True)

if "bot_started" not in st.session_state:
    thread = Thread(target=run_bot)
    thread.daemon = True
    thread.start()
    st.session_state.bot_started = True
