import streamlit as st
import requests

# ئەڤە لینکا تە یا نوو و دروستە
SERVER_URL = "https://accessed-textbook-arabia-morgan.trycloudflare.com"

st.set_page_config(page_title="Sidad AI 🐲", page_icon="🐲")
st.title("Sidad AI (Mîşkê Drinde) 🐲")

if prompt := st.chat_input("بێژە..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            res = requests.post(
                f"{SERVER_URL}/api/generate", 
                json={"model": "sidad-brain", "prompt": prompt, "stream": False},
                timeout=120
            )
            ans = res.json().get('response', 'بەرسڤ نەهات!')
            st.markdown(ans)
        except:
            st.error("تێرمۆکس یێ ڤەمراندییە!")
