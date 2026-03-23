import streamlit as st
from groq import Groq

# 1. ڕێکخستنا لاپەڕەی
st.set_page_config(page_title="Sidad Pro AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .main {
        direction: rtl;
        text-align: right;
    }
    </style>
    """, unsafe_allow_status=True)

st.title("🤖 Sidad Pro AI")
st.subheader("سیستەمێ ژیریێ دەستکرد ب بادینی (بێ سنۆر)")

# 2. وەرگرتنا کلیلێ ژ Secrets (دڤێت ل سایتێ Streamlit دانی)
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("کلیل (API Key) د ناڤ Secrets دا نینە! ژ کەرەما خۆ ل سایتێ Streamlit جێگیر بکە.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشاندانا نامێن بەری نوکە
for message in st.session
