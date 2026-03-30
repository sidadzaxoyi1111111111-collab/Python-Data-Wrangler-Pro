import streamlit as st
import requests

# ئەڤە ئەو لینکەیە کو تو لێ دگەڕێی (URL)
SERVER_URL = "https://mpeg-library-diameter-ways.trycloudflare.com"

st.set_page_config(page_title="Sidad AI", page_icon="🐲")
st.title("Sidad AI 🐲")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("سداد، تشتەکێ بنڤیسە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            payload = {"model": "sidad-brain", "prompt": prompt, "stream": False}
            response = requests.post(f"{SERVER_URL}/api/generate", json=payload, timeout=60)
            full_response = response.json().get('response', 'بەرسڤ نەهات!')
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except:
            st.error("پەیوەندی ب مۆبایلێ نەکەت! دڵنیا ببە Ollama و Cloudflared کار دکەن.")
