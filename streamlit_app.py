import streamlit as st
from groq import Groq

# وەرگرتنا کلیلێ ب شێوەیەکێ ئیمن
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("Error: API Key not found in Secrets!")
    st.stop()

client = Groq(api_key=api_key)

# بەردەوام بە ل سەر کۆدێ چاتێ وەک مە بەری نوکە نڤیسی...
