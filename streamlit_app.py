import streamlit as st
import requests
import json

# 1. Setup Page
st.set_page_config(page_title="Sidad AI Together", page_icon="⚡")
st.title("⚡ Sidad AI - Together Edition")
st.markdown("---")

# 2. API Key from Secrets
raw_api_key = st.secrets.get("GEMINI_KEY")

if not raw_api_key:
    st.error("⚠️ کلیل ل ناڤ Secrets نەهاتییە دیتن!")
else:
    # پشکنینا کلیلێ دا چو نڤیسینێن زێدە تێدا نەمینن
    api_key = raw_api_key.strip()

    if "messages" not in st.session_state:
        st.session_state.messages = []
        welcome = "سلاڤ! خێرهاتی بۆ ڤێرژنا پڕۆفیشناڵ یا **Sidad AI**. ئەز نوکە ب مێشکێ **Together AI** دئاخڤم."
        st.session_state.messages.append({"role": "assistant", "content": welcome})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. ڕێنماییا بادینی (Professional Badini Logic)
    badini_logic = (
        "You are Sidad AI, a highly professional AI assistant created by Sidad Ahmad from Zakho. "
        "STRICT LANGUAGE RULES: Speak ONLY in Badini Kurdish (Zakho dialect). "
        "NEVER use Sorani words. Use 'دکەم', 'دچم', 'چەوانی', 'دڤێت', 'سوپاس'. "
        "If the user speaks English, respond in professional academic English."
    )

    if prompt := st.chat_input("پسیارەکێ ب بادینی بکە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                url = "https://api.together.xyz/v1/chat/completions"
                
                # ئامادەکرنا داتایان
                payload = {
                    "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo", 
                    "messages": [
                        {"role": "system", "content": badini_logic},
                        *st.session_state.messages[-5:]
                    ],
                    "temperature": 0.4,
                    "max_tokens": 1024
                }
                
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }

                response = requests.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    response_text = result['choices'][0]['message']['content']
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                else:
                    # نیشاندانا خەتایێ ب ڕوونی
                    st.error(f"Together AI Error: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"Connection Error: {e}")

st.sidebar.markdown("---")
st.sidebar.write("Owner: **Sidad Ahmad**")
st.sidebar.write("Engine: **Together AI**")
