import streamlit as st
from groq import Groq
import requests  # فەرمانا ڕیقوێستس وەک تە داخواز کری

# 1. ڕێکخستنا لاپەرەی
st.set_page_config(page_title="Sidad AI - English Beast", layout="centered")

# 2. بارکرنا کلیلێ Groq ب پاراستی ژ Secrets
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    groq_client = Groq(api_key=GROQ_KEY)
except Exception as e:
    st.error("❌ GROQ_API_KEY is missing in Streamlit Secrets!")
    st.stop()

# --- ستایلێ سادە یێ لاپەرەی ---
st.title("🤖 Sidad AI - English Beast")
st.write("I am your English AI assistant. I do not talk about Binance.")
st.markdown("---")

# 3. پشکا چاتا زیرەک (AI Chat)
if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشاندانا نامەیێن کەفن
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# وەرگرتنا نامەیا نوو ژ بەکارهێنەری
user_input = st.chat_input("Ask me anything in English...")

if user_input:
    # زێدەکرنا نامەیا سداد بۆ لیستی
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # بەرسڤدان ب ڕێکا Groq
    with st.chat_message("assistant"):
        try:
            chat_completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are 'Sidad AI'. You ONLY speak English. Do NOT mention Binance or Crypto trading. Be smart and helpful to Sidad Ahmad Mohammed."
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
st.caption("Developed by Sidad | Powered by Groq AI")
