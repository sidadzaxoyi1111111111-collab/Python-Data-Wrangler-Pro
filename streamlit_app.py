import streamlit as st
import requests

# ئەڤە لینکا تە یا نوو یە
SERVER_URL = "https://empirical-wants-general-assistance.trycloudflare.com"

st.set_page_config(page_title="Sidad AI 🐲", page_icon="🐲")
st.title("Sidad AI (Mîşkê Drinde) 🐲")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("پسیارەکێ ژ بوتێ دڕندە بکە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # پەیوەندی دگەل مۆبایلا سدادی (Ollama)
            res = requests.post(
                f"{SERVER_URL}/api/generate", 
                json={"model": "sidad-brain", "prompt": prompt, "stream": False},
                timeout=60
            )
            ans = res.json().get('response', 'مێشکێ دڕندە بەرسڤ نەدا!')
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error("تێرمۆکس یێ ڤەمراندییە یان لینک یا ئێکسپایەر بوویە!")
