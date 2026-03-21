import streamlit as st
import requests
import json

# 1. Setup Page
st.set_page_config(page_title="Sidad AI Ultimate", page_icon="🧠")
st.title("🧠 Sidad AI - OpenRouter Stable")
st.markdown("---")

# 2. API Key from Secrets
api_key = st.secrets.get("GEMINI_KEY")

if not api_key:
    st.error("⚠️ کلیل ل ناڤ Secrets نەهاتییە دیتن!")
else:
    if "messages" not in st.session_state:
        st.session_state.messages = []
        welcome = "خێرهاتی بۆ **Sidad AI**. ئەز نوکە ب مێشکەکێ جێگیر یێ OpenRouter دئاخڤم."
        st.session_state.messages.append({"role": "assistant", "content": welcome})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. ڕێنماییا مێشکێ عیملاق
    badini_logic = (
        "You are Sidad AI, a professional assistant from Zakho. Creator: Sidad Ahmad.\n"
        "STRICT LANGUAGE: Speak ONLY in Badini Kurdish. Use 'دکەم', 'دچم', 'دڤێت', 'چەوانی', 'سوپاس'.\n"
        "If asked in English, use professional academic language."
    )

    if prompt := st.chat_input("پسیارەکێ بکە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # بکارئینانا مۆدێلا Gemma یا گوگل ل سەر OpenRouter (زۆر جێگیرە)
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://sidad-ai.streamlit.app", 
                        "X-Title": "Sidad AI",
                    },
                    data=json.dumps({
                        "model": "google/gemma-2-9b-it:free", 
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
                elif 'error' in result:
                    # ئەگەر خەتا دا، مۆدێلەکا دی تاقی بکە (Auto-fallback)
                    st.warning("مۆدێل مژوولە، دێ مۆدێلەکا دی تاقی کەین...")
                    # ل ڤێرێ دشێی مۆدێلا Mistral تاقی بکەی
                    st.error(f"OpenRouter Error: {result['error'].get('message')}")
                else:
                    st.error("بەرسڤ نەگەهشت، دبیت کلیل یا خەلەت بیت یان پارە تێدا نینە.")
                    
            except Exception as e:
                st.error(f"Connection Error: {e}")

st.sidebar.markdown("---")
st.sidebar.write("Owner: **Sidad Ahmad**")
st.sidebar.write("Engine: **Gemma 2 Stable**")
