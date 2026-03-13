import streamlit as st
import telebot
from threading import Thread

# 1. لێرە تەوکنێ بۆتێ خۆ دانیە
BOT_TOKEN = "لێرە_تەوکنێ_بۆتێ_خۆ_دانیە"
bot = telebot.TeleBot(BOT_TOKEN)

# ئەڤە بۆ دیزاینا سایتێ تە ل سەر ستریملێت
st.title("🚀 AI Data Operations Dashboard")
st.write("سیداد برا، بۆتێ تە و سایتێ تە نوکە یێ کار دکەن!")
st.metric(label="Bot Status", value="Active", delta="Running 24/7")

# فرمانا بۆتی
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "سڵاو سیداد! بۆتێ تە ل سەر Render ب سەرکەفتی کەفتە کار.")

# کارپێکرنا بۆتی د باکگراوەندی دا
def run_bot():
    bot.polling(none_stop=True)

if "bot_started" not in st.session_state:
    thread = Thread(target=run_bot)
    thread.start()
    st.session_state.bot_started = True
