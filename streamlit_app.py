import streamlit as st
import requests

# ناڤ و نیشانێن سایتێ تە
st.set_page_config(page_title="Sidad AI Badini", page_icon="🤖")

st.title("🤖 Sidad AI - ب بادینی")
st.write("سڵاو سداد! ئەڤە پڕۆژەیێ تە یێ نوویە ب بەکارئینانا کلیلا ChatAnywhere.")

# وەرگرتنا کلیلێ ژ Secrets
if "CHATANYWHERE_API_KEY" in st.secrets:
    API_KEY = st.secrets["CHATANYWHERE_API_KEY"]
    URL = "https://api.chatanywhere.tech/v1/chat/completions"
    
    # دروستکرنا چاتێ
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # نیشاندانا نامەیێن کۆن
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # وەرگرتنا نامەیا نوو ژ بەکارهێنەری
    if prompt := st.chat_input("چ ل دەف تە هەیە سداد؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # ناردنا داخوازییێ (Request) بۆ API
        with st.chat_message("assistant"):
            headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": st.session_state.messages
            }
            
            try:
                response = requests.post(URL, headers=headers, json=payload)
                if response.status_code == 200:
                    full_response = response.json()['choices'][0]['message']['content']
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.error(f"خەتایەک هەیە: {response.status_code}")
            except Exception as e:
                st.error(f"پەیوەندی دروست نەبوو: {e}")
else:
    st.warning("تکایە کلیلا API د بەشێ Secrets دا دابنێ.")
