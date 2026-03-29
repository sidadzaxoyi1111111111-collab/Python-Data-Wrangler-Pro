import streamlit as st
from groq import Groq
import os

# --- ١. خواندنا کلیلێ ب شێوەیەکێ پاراستی ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("❌ سداد برا، کلیل د پشکا Secrets دا نینە!")
    st.stop()

# --- ٢. ڕێکخستنا شاشێ ---
st.set_page_config(page_title="Sidad AI - Pro", layout="centered")

# CSS بۆ ڕێکخستنا نڤیسینا کوردی (RTL)
st.markdown("""
    <style>
    .stChatMessage { direction: rtl; font-family: 'Arial'; }
    .stChatInput { direction: rtl; }
    div[data-testid="stChatMessageContent"] { text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.title("Sidad AI - Python Expert 🐍")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- ٣. نیشاندانا نامەیان ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- ٤. جهێ نڤیسینا نامەیێ (چەوان نامێ بۆ بهنێری) ---
# سداد برا، تەنێ ل ڤێرە بنڤیسە و ئینتەر بکە
if prompt := st.chat_input("نامەیا خۆ لێرە بنڤیسە سداد برا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- ٥. وەرگرتنا بەرسڤێ ژ Groq ---
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {
                    "role": "system", 
                    "content": "Tu Sidad AI yî. Pisporê Python î. Bi tenê bi kurdîya Behdînî (tîpên erebî) bersivê bide. Bersivên te bila kurt û zelal bin."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        bot_response = completion.choices[0].message.content
    except Exception as e:
        bot_response = f"⚠️ خەلەتیەک: {str(e)}"

    with st.chat_message("assistant"):
        st.markdown(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
