import streamlit as st
import requests  # فەرمانا ڕیقوێستس وەک تە داخواز کری
from groq import Groq

# 1. ڕێکخستنا لاپەرەی
st.set_page_config(page_title="Sidad AI - English Beast", page_icon="🦾")

# 2. بارکرنا کلیلێ Groq ب پاراستی
try:
    GROQ_KEY = st.secrets["GROQ_KEY"]
    groq_client = Groq(api_key=GROQ_KEY)
    st.sidebar.success("✅ AI Mode: Online")
except Exception as e:
    st.sidebar.error("❌ Secrets Missing: Check GROQ_KEY")
    st.stop()

# --- ستایلێ لاپەرەی ---
st.title("🦾 Sidad AI - Wall Street Beast")
st.markdown("---")

# 3. پشکا چاتا زیرەک (Chat System)
if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشاندانا نامەیێن کەفن
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# وەرگرتنا نامەیێ ب ئینگلیزی
user_input = st.chat_input("Ask me about the market in English...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            # بانگا Groq دکەین بۆ بەرسڤدانێ
            chat_completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are 'The Wall Street Beast'. You ONLY speak English. You are helping Sidad Ahmad Mohammed. Be smart, professional, and provide top-tier market insights."
                    },
                    *st.session_state.messages
                ]
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"AI Error: {e}")

st.markdown("---")
st.caption("Developed by Sidad | Powered by Groq AI | 2026")
