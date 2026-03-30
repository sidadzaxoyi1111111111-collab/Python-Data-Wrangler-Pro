import streamlit as st
import requests

# لینکێ تە یێ نوو یێ Cloudflare
SERVER_URL = "https://old-yellow-evaluations-rebel.trycloudflare.com"

# ڕێکخستنا لاپەڕەی
st.set_page_config(page_title="Sidad AI 🐲", page_icon="🐲")
st.title("Sidad AI (Mîşkê Drinde) 🐲")

# پاراستنا نامەیێن کۆن (Chat History)
if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشاندانا نامەیێن بەری نوکە
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# وەرگرتنا پسیارا نوو ژ بەکارهێنەری
if prompt := st.chat_input("پسیارەکێ ژ بوتێ دڕندە بکە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # ناردنا پسیارێ بۆ مۆبایلا سدادی (Ollama)
            response = requests.post(
                f"{SERVER_URL}/api/generate", 
                json={
                    "model": "sidad-brain", 
                    "prompt": prompt, 
                    "stream": False
                },
                timeout=120 # دەمێ پێدڤی بۆ مێشکێ 8.5GB
            )
            
            if response.status_code == 200:
                ans = response.json().get('response', 'بەرسڤ نەهاتە وەرگرتن!')
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            else:
                st.error(f"کێشەیەک هەبوو: {response.status_code}")
                
        except Exception as e:
            st.error("تێرمۆکس یێ ڤەمراندییە یان لینک یا ئێکسپایەر بوویە! دڵنیا ببە cloudflared یا کارە.")

