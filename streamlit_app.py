import streamlit as st
from groq import Groq
import requests
import os

# --- ١. خواندنا کلیلێ ژ Secrets ب شێوەیەکێ پاراستی ---
try:
    # پێدڤییە ناڤێ کلیلێ د Secrets دا "GROQ_API_KEY" بیت
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("❌ سداد برا، کلیل د پشکا Secrets دا نەهاتییە دیتن! ناڤێ وێ بکە GROQ_API_KEY")
    st.stop()

# --- ٢. ڕێکخستنا شاشا سایتێ سداد ---
st.set_page_config(page_title="Sidad AI - Multi-Language", layout="centered")

# CSS بۆ جوانکرنا نڤیسینێ و ئاراستێ وێ
st.markdown("""
    <style>
    .stChatMessage { font-family: 'Arial'; }
    </style>
    """, unsafe_allow_html=True)

st.title("Sidad AI - Smart Chat 🚀")

# دروستکرنا مێژوویەکێ بۆ نامەیان
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- ٣. نیشاندانا نامەیان ب شێوازێ واتس ئەپ (Bubble Style) ---
for message in st.session_state.messages:
    align = "right" if message["role"] == "user" else "left"
    bg_color = "#dcf8c6" if message["role"] == "user" else "#ffffff"
    direction = "rtl" if any("\u0600" <= c <= "\u06FF" for c in message["content"]) else "ltr"
    label = "تۆ" if message["role"] == "user" else "Sidad AI"
    
    st.markdown(f"""
        <div style='text-align: {align}; direction: {direction};'>
            <div style='display: inline-block; background-color: {bg_color}; padding: 12px; border-radius: 15px; margin: 5px; color: black; border: 1px solid #ddd; max-width: 85%; box-shadow: 1px 1px 3px rgba(0,0,0,0.1);'>
                <small style='color: gray; font-weight: bold;'>{label}</small><br>
                {message["content"]}
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- ٤. جهێ نڤیسینا نامەیێ (Chat Input) ---
if prompt := st.chat_input("نامەیا خۆ بنڤیسە... Write your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# --- ٥. وەرگرتنا بەرسڤێ ژ Groq (Llama 3.1) ---
if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    user_input = st.session_state.messages[-1]["content"]
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {
                    "role": "system", 
                    "content": """You are Sidad AI, a smart assistant. 
                    - If the user speaks in Kurdish/Badini, reply ONLY in clear Kurdish Badini dialect. 
                    - If the user speaks in English, reply ONLY in English. 
                    - Keep your answers helpful and professional."""
                },
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
        )
        bot_response = completion.choices[0].message.content
    except Exception as e:
        bot_response = f"⚠️ Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.rerun()

# --- ٦. لایێSidebar (بۆ زانیاریێن زێدە) ---
with st.sidebar:
    st.header("📊 Dashboard")
    if os.path.exists("chart.png"):
        st.image("chart.png", caption="Market Chart")
    else:
        st.info("No chart.png found on GitHub.")
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
