import streamlit as st
from groq import Groq
import os

# --- ڕێکخستنا Groq ---
# سداد برا، ل ڤێرە کلیلا خۆ یا Groq دابنێ
client = Groq(api_key="لێرە_کلیلێ_Groq_دابنێ")

st.set_page_config(page_title="Sidad AI - Groq Mode", layout="centered")
st.title("Sidad AI - Groq Powered ⚡")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- نیشاندانا نامەیان ب شێوازێ واتس ئەپ ---
for chat in st.session_state.chat_history:
    align = "right" if chat["role"] == "user" else "left"
    bg_color = "#dcf8c6" if chat["role"] == "user" else "#ffffff"
    label = "تۆ" if chat["role"] == "user" else "Sidad AI"
    
    st.markdown(f"""
        <div style='text-align: {align};'>
            <div style='display: inline-block; background-color: {bg_color}; padding: 10px; border-radius: 10px; margin: 5px; color: black; border: 1px solid #ddd; max-width: 80%;'>
                <b>{label}:</b> {chat['content']}
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- جهێ نڤیسینا نامەیێ ---
user_input = st.chat_input("نامەیا خۆ بنڤیسە...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    try:
        # داخوازکرنا بەرسڤێ ژ Groq (Llama 3)
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "تو بوتەکێ ژیری ناڤێ تە Sidad AI یە، ب کوردییا بەدینی بەرسڤێ بدە."},
                {"role": "user", "content": user_input}
            ],
        )
        bot_response = completion.choices[0].message.content
    except Exception as e:
        bot_response = "ببۆره سداد برا، کێشەیەک د کلیلا Groq دا هەیە!"

    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
    st.rerun()
