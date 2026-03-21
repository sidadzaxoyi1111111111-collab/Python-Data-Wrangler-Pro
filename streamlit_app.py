import streamlit as st
import requests
import json

# 1. Setup Page
st.set_page_config(page_title="Sidad AI Ultimate", page_icon="🧠")
st.title("🧠 Sidad AI - OpenRouter Edition")
st.markdown("---")

# 2. API Key from Secrets
api_key = st.secrets.get("GEMINI_KEY")

if not api_key:
    st.error("⚠️ API Key is missing!")
else:
    if "messages" not in st.session_state:
        st.session_state.messages = []
        welcome = "خێرهاتی بۆ هێزا عیملاق یا **Sidad AI**. ئەز نوکە ب ڕێکا OpenRouter دئاخڤم. How can I assist you?"
        st.session_state.messages.append({"role": "assistant", "content": welcome})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. ڕێنماییا مێشکێ عیملاق (Professional Logic)
    badini_logic = (
        "You are Sidad AI, a super-intelligent assistant from Zakho. Creator: Sidad Ahmad.\n"
        "STRICT LANGUAGE: Speak ONLY in Badini Kurdish dialect. NEVER use Sorani like 'دەکەم' or 'دەچم'.\n"
        "Use 'دکەم', 'دچم', 'دڤێت', 'چەوانی', 'سوپاس'.\n"
        "If the user asks in English, be very professional and academic."
    )

    if prompt := st.chat_input("پسیارەکێ بکە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # بانگکرنا OpenRouter API
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    data=json.dumps({
                        "model": "meta-llama/llama-3.3-70b:free", 
                        "messages": [
                            {"role": "system", "content": badini_logic},
                            *st.session_state.messages[-5:]
                        ]
                    })
                )
                
                result = response.json()
                response_text = result['choices'][0]['message']['content']
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Error: {e}")

st.sidebar.markdown("---")
st.sidebar.write("Owner: **Sidad Ahmad**")
st.sidebar.write("Platform: **OpenRouter**")
