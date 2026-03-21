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
    st.error("⚠️ کلیل ل ناڤ Secrets نەهاتییە دیتن!")
else:
    if "messages" not in st.session_state:
        st.session_state.messages = []
        welcome = "خێرهاتی بۆ هێزا عیملاق یا **Sidad AI**. ئەز نوکە ب ڕێکا OpenRouter دئاخڤم."
        st.session_state.messages.append({"role": "assistant", "content": welcome})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. ڕێنماییا مێشکێ عیملاق (Professional Logic)
    badini_logic = (
        "You are Sidad AI, a professional assistant from Zakho. Creator: Sidad Ahmad.\n"
        "STRICT LANGUAGE: Speak ONLY in Badini Kurdish dialect. Use 'دکەم', 'دچم', 'دڤێت', 'چەوانی', 'سوپاس'."
    )

    if prompt := st.chat_input("پسیارەکێ بکە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # بکارئینانا مۆدێلەکا جێگیر و ب بێ بەرامبەر
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "http://localhost:8501", # پێتڤییە بۆ OpenRouter
                        "X-Title": "Sidad AI",
                    },
                    data=json.dumps({
                        "model": "meta-llama/llama-3.1-8b-instruct:free", # ئەڤە مۆدێلەکا زۆر جێگیرە
                        "messages": [
                            {"role": "system", "content": badini_logic},
                            *st.session_state.messages[-5:]
                        ]
                    })
                )
                
                result = response.json()
                
                if 'choices' in result:
                    response_text = result['choices'][0]['message']['content']
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                else:
                    error_msg = result.get('error', {}).get('message', 'Unknown Error')
                    st.error(f"OpenRouter Error: {error_msg}")
                    
            except Exception as e:
                st.error(f"Connection Error: {e}")

st.sidebar.markdown("---")
st.sidebar.write("Owner: **Sidad Ahmad**")
st.sidebar.write("Model: **Llama 3.1 8B Free**")
