import streamlit as st
import google.generativeai as genai
import os

# Setup Page
st.set_page_config(page_title="Sidad AI - Gemini 1.5", page_icon="🤖")
st.title("🤖 Sidad AI - Gemini 1.5 Flash")

# Get API Key from Secrets
api_key = st.secrets.get("GEMINI_KEY")

if not api_key:
    st.error("Error: API Key not found in Streamlit Secrets!")
else:
    genai.configure(api_key=api_key)
    
    # Use Gemini 1.5 Flash for better stability
    model = genai.GenerativeModel('gemini-1.5-flash')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("...پسیارەکێ بکە"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # System instruction for Badini dialect
                full_prompt = f"بەرسڤێ ب زمانی کوردی بادینی بدە: {prompt}"
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")
