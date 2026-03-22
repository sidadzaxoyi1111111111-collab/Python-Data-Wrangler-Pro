import streamlit as st
import google.generativeai as genai

# ١. خواندنا کلیلێ ژ جهێ نهێنی (Secrets)
# ئێدی کلیل ل ڤێرە دیار نابیت و کەس نەشێت بدۆزیتەوە
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# باقیا کۆدی وەکی خۆ بمینیت...
st.title("🐍 Sidad AI 2.0 (Secured)")

if prompt := st.chat_input("تشتەکێ بنڤیسە..."):
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        full_prompt = f"بەرسڤا ڤێ نامەیێ ب تنێ ب دیالەکتا کوردی بادینی بدە: {prompt}"
        response = model.generate_content(full_prompt)
        st.markdown(response.text)
