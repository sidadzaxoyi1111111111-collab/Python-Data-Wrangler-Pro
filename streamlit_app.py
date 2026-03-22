import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Sidad AI Pro", page_icon="🐍")

st.title("🐍 Sidad Python Pro AI")
st.write("بخێر بێی بۆ پلاتفۆرمێ من یێ ژیرییا دەستکرد")

# ل ڤێرە کلیلێ خۆ دانێ
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

user_input = st.text_input("پسیارەکێ ب بادینی ژ من بکە:")

if user_input:
    response = model.generate_content(f"بەرسڤ بدە ب دیالەکتا بادینی: {user_input}")
    st.info(response.text)
