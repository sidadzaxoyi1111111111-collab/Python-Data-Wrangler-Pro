import streamlit as st
import google.generativeai as genai

# ١. خواندنا کلیلێ ب شێوەیەکێ پاراستی
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("کلیل ل ناڤ Secrets نەهاتییە دیتن!")
    st.stop()

st.title("🐍 Sidad AI 2.0")

# ٢. سیستەمێ چاتێ
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تشتەکێ بنڤیسە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        full_prompt = f"بەرسڤ بدە ب دیالەکتا بادینی: {prompt}"
        response = model.generate_content(full_prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
