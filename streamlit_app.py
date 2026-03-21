import streamlit as st
import google.generativeai as genai

# 1. ڕێکخستنا لاپەڕەی
st.set_page_config(page_title="Sidad AI", page_icon="🤖")
st.title("🤖 Sidad AI - Gemini 1.5 Flash")

# 2. ئینانا کلیلێ (API Key) ژ Secrets
api_key = st.secrets.get("GEMINI_KEY")

if not api_key:
    st.error("⚠️ کلیل (API Key) نەهاتییە دیتن! ل ناڤ Secrets دانێ.")
else:
    # ڕێکخستنا گوگل
    genai.configure(api_key=api_key)
    
    # ڤێرژنا گونجای یا مۆدێلێ دا خەتایا 404 نەمینیت
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("پسیارەکێ بکە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # فەرمانا زمانێ بادینی
                response = model.generate_content(f"تۆ Sidad AI، ب زمانی کوردی بادینی بەرسڤێ بدە: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # ئەگەر هەر خەتا دا، ڤێرژنەکێ دی تاقی بکە
                st.error(f"Error: {e}")

st.sidebar.write("Developed by: **Sidad Ahmad**")
