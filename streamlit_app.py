import streamlit as st
from groq import Groq
import os

# --- خواندنا کلیلێ ژ Secrets ب شێوەیەکێ پاراستی ---
try:
    # ل ڤێرە ناڤێ کلیلێ د Secrets دا پێدڤییە "GROQ_API_KEY" بیت
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception as e:
    st.error("سداد برا، کلیل د پشکا Secrets دا نەهاتییە دیتن! تکایە ناڤێ وێ ب دروستی بنڤیسە.")
    st.stop()

st.set_page_config(page_title="Sidad AI - WhatsApp Style", layout="centered")
st.title("Sidad AI - Groq Powered ⚡")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- نیشاندانا نامەیان (واتس ئەپ) ---
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
user_input = st.chat_input("نامەیا خۆ لێرە بنڤیسە سداد برا...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    try:
        # داخوازکرنا بەرسڤێ ژ مۆدێلا Llama 3 یا خێرا
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "تو بوتەکێ ژیری ناڤێ تە Sidad AI یە، ب کوردییا بەدینی بەرسڤێ بدە."},
                {"role": "user", "content": user_input}
            ],
        )
        bot_response = completion.choices[0].message.content
    except Exception as e:
        bot_response = f"خەلەتیەک چێبوو: {str(e)}"

    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
    st.rerun()
