import streamlit as st
import requests
import json

# --- بانگکرنا کلیلێ ژ Secrets ---
# ل ڤێرێ مە ناڤێ کلیلێ کرییە "OPENROUTER_API_KEY"
API_KEY = st.secrets["OPENROUTER_API_KEY"]

st.set_page_config(page_title="Sidad AI Agent", page_icon="🤖")
st.title("🤖 Sidad AI Pro Agent")
st.markdown("بخێر بێی بۆ بۆتێ من یێ نوی یێ بهێز!")

# دروستکرنا جهێ چاتی (Chat History)
if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشاندانا نامەیێن بەری نوکە
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# وەرگرتنا نامەیا نوی ژ بەکارهێنەری
if prompt := st.chat_input("پسیارا تە چییە؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # پەیوەندی ب OpenRouter API
    with st.chat_message("assistant"):
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "openchat/openchat-7b:free",
            "messages": st.session_state.messages
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                full_response = response.json()['choices'][0]['message']['content']
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error(f"Error: {response.status_code}")
        except Exception as e:
            st.error(f"Connection Error: {e}")
