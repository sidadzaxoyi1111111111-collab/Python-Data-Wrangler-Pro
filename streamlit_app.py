import streamlit as st
import requests
import json

# 1. Setup Page
st.set_page_config(page_title="Sidad AI Together", page_icon="⚡")
st.title("⚡ Sidad AI - Together Edition")
st.markdown("---")

# 2. API Key from Secrets
api_key = st.secrets.get("GEMINI_KEY")

if not api_key:
    st.error("⚠️ API Key is missing in Secrets!")
else:
    if "messages" not in st.session_state:
        st.session_state.messages = []
        welcome = "سلاڤ! خێرهاتی بۆ ڤێرژنا پڕۆفیشنال یا **Sidad AI**. ئەز نوکە ب مێشکەکێ Together AI دئاخڤم."
        st.session_state.messages.append({"role": "assistant", "content": welcome})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. ڕێنماییا مێشکێ عیملاق (Professional Badini)
    badini_logic = (
        "You are Sidad AI, a highly professional AI assistant created by Sidad Ahmad. "
        "STRICT LANGUAGE RULES: Speak ONLY in Badini Kurdish (Zakho/Duhok dialect). "
        "NEVER use Sorani words like 'دەکەم', 'دەچم', 'چۆنیت'. "
        "Use 'دکەم', 'دچم', 'چەوانی', 'دڤێت', 'سوپاس'. "
        "If the user speaks English, respond in professional academic English."
    )

    if prompt := st.chat_input("پسیارەکێ ب بادینی بکە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # بانگکرنا Together AI API
                url = "https://api.together.xyz/v1/chat/completions"
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
                    st.error(f"Together AI Error: {response.text}")

            except Exception as e:
                st.error(f"Connection Error: {e}")

st.sidebar.markdown("---")
st.sidebar.write("Owner: **Sidad Ahmad**")
st.sidebar.write("Engine: **Together AI (Llama 3.3)**")
