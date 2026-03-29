import streamlit as st
from groq import Groq

# ١. گرێدانا کلیلێ ب پاراستی ژ Secrets
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

st.title("🤖 Sidad AI - English & Badini")

# ٢. مۆدێلێ نوو و جێگیر
MODEL = "llama-3.3-70b-versatile"

def sidad_chat(user_text):
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system", 
                    "content": "You are Sidad AI. Always reply in English followed by the Kurdish Badini dialect. Be smart and professional."
                },
                {"role": "user", "content": user_text}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error / خەلەتی: {e}"

# ٣. شاشا چاتی
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Write here... ل ڤێرێ بنڤیسە"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Sidad AI is processing..."):
            response = sidad_chat(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
