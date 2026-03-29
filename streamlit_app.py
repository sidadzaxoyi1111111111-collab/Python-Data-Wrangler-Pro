import streamlit as st
from groq import Groq

# ١. کێشانا کلیلێ ژ Secrets
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

st.title("🤖 Sidad AI - English & Badini")

# ٢. مۆدێلێ جێگیر
MODEL = "llama-3.3-70b-versatile"

def sidad_chat(text_input): # ل ڤێرە مە گۆڕاو پێناسە کر
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system", 
                    "content": "You are Sidad AI. Answer in English first, then in Kurdish Badini dialect (Zakho/Duhok style). Be smart and helpful."
                },
                {"role": "user", "content": text_input} # ڤێرە ڕاست بوو
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error / خەلەتی: {e}"

# ٣. دروستکرنا شاشا چاتی
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# وەرگرتنا نامەیێ ژ سدادی
if prompt := st.chat_input("Write here... ل ڤێرێ بنڤیسە"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Sidad AI is processing..."):
            # مە 'prompt' فرێکرە ناڤ فۆنکشنێ دا خەلەتی نەمینیت
            response = sidad_chat(prompt) 
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
