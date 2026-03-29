import streamlit as st
from groq import Groq
import requests
import os

# --- ١. خواندنا کلیلێ ژ Secrets ب شێوەیەکێ پاراستی ---
try:
    # پشتراستبە ناڤێ کلیلێ د Secrets دا "GROQ_API_KEY" بیت
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("❌ سداد برا، کلیل د پشکا Secrets دا نەهاتییە دیتن! ناڤێ وێ بکە GROQ_API_KEY")
    st.stop()

# --- ٢. ڕێکخستنا شاشا سایتێ سداد ---
st.set_page_config(page_title="Sidad AI - WhatsApp Style", layout="centered")

# ستایلەکێ سادە بۆ جوانکرنا چاتی
st.markdown("""
    <style>
    .stChatMessage { direction: rtl; }
    .stChatInput { direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("Sidad AI - Groq Powered ⚡")

# دروستکرنا مێژوویەکێ بۆ نامەیان
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- ٣. نیشاندانا نامەیان ب شێوازێ واتس ئەپ (Bubble Style) ---
for message in st.session_state.messages:
    align = "right" if message["role"] == "user" else "left"
    bg_color = "#dcf8c6" if message["role"] == "user" else "#ffffff"
    label = "تۆ" if message["role"] == "user" else "Sidad AI"
    
    st.markdown(f"""
        <div style='text-align: {align};'>
            <div style='display: inline-block; background-color: {bg_color}; padding: 10px; border-radius: 10px; margin: 5px; color: black; border: 1px solid #ddd; max-width: 80%; direction: rtl; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);'>
                <small style='color: gray;'>{label}</small><br>
                {message["content"]}
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- ٤. جهێ نڤیسینا نامەیێ (Chat Input) ---
if prompt := st.chat_input("نامەیا خۆ لێرە بنڤیسە سداد برا..."):
    # زێدەکرنا نامەیا تە بۆ مێژوویێ
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # نیشاندانا دەستبەجێ یا نامەیا تە ل سەر شاشێ
    st.rerun()

# --- ٥. وەرگرتنا بەرسڤێ ژ Groq ---
if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    user_input = st.session_state.messages[-1]["content"]
    
    try:
        # داخوازکرنا بەرسڤێ ژ مۆدێلا نوی (Llama 3.1)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {"role": "system", "content": "تو بوتەکێ ژیری ناڤێ تە Sidad AI یە، ب کوردییا بەدینی بەرسڤێ بدە."},
                {"role": "user", "content": user_input}
            ],
        )
        bot_response = completion.choices[0].message.content
    except Exception as e:
        bot_response = f"⚠️ خەلەتیەک چێبوو سداد برا: {str(e)}"

    # زێدەکرنا بەرسڤا بوتێ بۆ مێژوویێ
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.rerun()

# --- ٦. پشکا وێنەی (ئەگەر هەبیت) ل لایێ Sidebar ---
with st.sidebar:
    st.header("📊 زانیاریێن زێدە")
    if os.path.exists("chart.png"):
        st.image("chart.png", caption="📈 ئاستێ نرخێ بازارێ باینانس")
    else:
        st.info("سداد برا، فایلێ chart.png ل سەر GitHub نینە.")
