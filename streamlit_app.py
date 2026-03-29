import streamlit as st
from groq import Groq
import requests
import os

# --- ١. خواندنا کلیلێ ب شێوەیەکێ پاراستی ---
try:
    # پێدڤییە ناڤێ کلیلێ د Secrets دا "GROQ_API_KEY" بیت
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("❌ سداد برا، کلیل د پشکا Secrets دا نەهاتییە دیتن! ناڤێ وێ بکە GROQ_API_KEY")
    st.stop()

# --- ٢. ڕێکخستنا شاشا سایتێ سداد ---
st.set_page_config(page_title="Sidad AI - Pro Expert", layout="centered")

# CSS بۆ جوانکرنا نڤیسینێ و پشتگیرییا زمانێ کوردی
