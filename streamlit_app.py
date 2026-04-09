import streamlit as st
from groq import Groq

# --- بانگکرنا کلیلێ ژ Secrets ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("⚠️ کلیلا Groq نەهاتییە دیتن! ل Secrets زێدە بکە.")

st.title("🤖 Sidad AI Master (Powered by Groq)")

# --- مێشکێ بۆتی ---
system_prompt = "You are Sidad AI Master. Expert in Kali Linux, CyberSecurity, All Programming languages, and Multi-languages. Answer clearly and technically."

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("فەرموو سداد..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # ل ڤێرێ Groq وەڵامێ ددەت (زۆر خێرا)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                *st.session_state.messages
            ],
            model="llama-3.3-70b-versatile", # مۆدێلا هەرە ب هێز یا Groq
        )
        response = chat_completion.choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
