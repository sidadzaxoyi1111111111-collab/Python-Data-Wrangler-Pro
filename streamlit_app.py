import streamlit as st
import telebot
import requests
import threading

# --- ڕێکخستنا لاپەڕێ سایتێ سداد ---
st.set_page_config(page_title="Sidad AI Badini Pro", page_icon="🤖")
st.title("🤖 Sidad AI Dashboard")
st.write("سڵاو سداد! ئەڤە پڕۆژەیێ تە یێ تێلێگرامێ و سایتێ تە یە ب بادینی.")

# --- وەرگرتنا کلیلان ژ Secrets ---
if "CHATANYWHERE_API_KEY" in st.secrets and "TELEGRAM_BOT_TOKEN" in st.secrets:
    AI_KEY = st.secrets["CHATANYWHERE_API_KEY"]
    BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
    AI_URL = "https://api.chatanywhere.tech/v1/chat/completions"

    bot = telebot.TeleBot(BOT_TOKEN)

    # --- سیستەمێ ڕێنماییا بادینی (System Prompt) ---
    # ئەڤە دەستوورە بۆ AI دا تەنێ ب بادینی باخڤیت
    BADINI_INSTRUCTIONS = (
        "تو یاریدەدەرەکێ زیرەکی و ناڤێ تە Sidad AI یە. "
        "تەنێ و تەنێ ب زارۆکێ کوردییا بادینی (بەهدینی) بەرسڤێ بدە. "
        "ب چو ڕەنگان ب سۆرانی نەئاخڤە. "
        "ب شوونا 'باشە' بێژە 'گەلەک باشە' یان 'دروستە'. "
        "ب شوونا 'ئێستا' بێژە 'نوکە'. "
