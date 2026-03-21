import streamlit as st
from google import genai
import os

# وەرگرتنا کلیلێ ب شێوەیەکێ پاراستی
GEMINI_KEY = os.getenv('GEMINI_KEY')

st.set_page_config(page_title="Sidad AI", page_icon="🤖")
st.title("🤖 Sidad AI - Gemini 2.0")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("پسیارەکێ بکە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        client = genai.Client(api_key=GEMINI_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"تۆ یاریدەدەرێکی زیرەکی، بە زمانی کوردی بادینی وەڵامی ئەمە بدەوە: {prompt}"
        )
        with st.chat_message("assistant"):
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")
