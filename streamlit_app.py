import streamlit as st
import google.generativeai as genai

# 1. Setup Page
st.set_page_config(page_title="Sidad AI", page_icon="🤖")
st.title("🤖 Sidad AI - Gemini 1.5 Flash")

# 2. Get API Key from Secrets
api_key = st.secrets.get("GEMINI_KEY")

if not api_key:
    st.error("⚠️ کلیل (API Key) نەهاتییە دیتن! بچۆ ناڤ Secrets و دانێ.")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 3. Chat Session State
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 4. Chat Input
    if prompt := st.chat_input("پسیارەکێ بکە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # System instruction within the prompt
                response = model.generate_content(f"تۆ Sidad AI، ب زمانی کوردی بادینی بەرسڤێ بدە: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")

# Footer
st.sidebar.write("Developed by: **Sidad Ahmad**")
