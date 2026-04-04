import streamlit as st
import requests
import json

# --- 1. ڕێکخستنا لاپەرەی ---
st.set_page_config(page_title="Sidad AI Pro Agent", page_icon="🤖", layout="centered")

# --- 2. وەرگرتنا کلیلێ ژ Secrets ---
# ل دێشبۆردێ Streamlit د پشکا Secrets دا بنڤێسە: OPENROUTER_API_KEY = "کلیل"
if "OPENROUTER_API_KEY" in st.secrets:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
else:
    st.error("کلیل د Secrets دا نەهاتییە دیتن! تکایە کلیلێ ل دێشبۆردێ Streamlit زێدە بکە.")
    st.stop()

# --- 3. دیزاینا دەرڤە (UI) ---
st.title("🤖 Sidad AI Pro Agent")
st.markdown("---")
st.info("بخێر بێی بۆ بۆتێ من یێ نوی یێ بهێز! ئەڤە پڕۆژێ من یێ پایتۆنە.")

# --- 4. دروستکرنا بیردانکا چاتی (Chat History) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشاندانا نامەیێن کۆن د ناڤ لاپەرەی دا
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. وەرگرتنا نامەیا نوی ژ بەکارهێنەری ---
if prompt := st.chat_input("پسیارا تە چییە سداد؟"):
    # زێدەکرنا نامەیا تە بۆ لیستێ
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- 6.
