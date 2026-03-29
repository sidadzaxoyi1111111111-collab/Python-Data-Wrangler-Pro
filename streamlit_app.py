import streamlit as st
import os

# ڕێکخستنا سەرەکی یا لاپەڕی
st.set_page_config(page_title="Sidad AI Chat", layout="centered")

st.title("Sidad AI - WhatsApp Style 💬")

# لێرە مێژوویا نامەیان پاشەکەفت دکەین
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- نیشاندانا نامەیان ب شێوازێ واتس ئەپ ---
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        # نامەیا تە (ل لایێ ڕاست)
        st.markdown(f"<div style='text-align: right; background-color: #dcf8c6; padding: 10px; border-radius: 10px; margin: 5px; color: black;'><b>تۆ:</b> {chat['content']}</div>", unsafe_allow_html=True)
    else:
        # نامەیا بوتێ تە (ل لایێ چەپ)
        st.markdown(f"<div style='text-align: left; background-color: #ffffff; padding: 10px; border-radius: 10px; border: 1px solid #ddd; margin: 5px; color: black;'><b>بوت:</b> {chat['content']}</div>", unsafe_allow_html=True)

# --- جهێ نڤیسینا نامەیێ (وەکی واتس ئەپ) ---
with st.container():
    user_input = st.chat_input("نامەیا خۆ لێرە بنڤیسە سداد برا...")
    
    if user_input:
        # زێدەکرنا نامەیا تە بۆ مێژوویێ
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # دروستکرنا وەڵاما بوتێ تە
        bot_response = f"نامەیا تە گەهشت سداد: '{user_input}'. ئەز نوکە داتایێن باینانس پشکنین دکەم..."
        st.session_state.chat_history.append({"role": "bot", "content": bot_response})
        
        # دووبارە ڕەنکرنا لاپەڕی دا نامەیێن نوی دیار بن
        st.rerun()

# --- نیشاندانا وێنەی ل خوارێ ---
st.divider()
if os.path.exists("chart.png"):
    st.image("chart.png", caption="چارتێ بازاڕی یێ SOL")
