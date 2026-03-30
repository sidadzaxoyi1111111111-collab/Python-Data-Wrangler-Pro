import streamlit as st
import requests

# لینکێ تە یێ نوو یێ Cloudflare کو د تێرمۆکس دا دیار بووی
SERVER_URL = "https://old-yellow-evaluations-rebel.trycloudflare.com"

st.set_page_config(page_title="Sidad AI 🐲", page_icon="🐲")
st.title("Sidad AI (Mîşkê Drinde) 🐲")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("بێژە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # پەیوەندی دگەل مۆبایلا سدادی (Ollama)
            res = requests.post(
                f"{SERVER_URL}/api/generate", 
                json={
                    "model": "sidad-brain", 
                    "prompt": prompt, 
                    "stream": False
                },
                timeout=120
            )
            ans = res.json().get('response', 'مێشکێ دڕندە بەرسڤ نەدا!')
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except:
            st.error("تێرمۆکس یێ ڤەمراندی یە یان لینک یا گوهۆڕی یە!")
