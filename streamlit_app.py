import streamlit as st
from groq import Groq

# 1. Config
st.set_page_config(page_title="Sidad Pro AI", page_icon="🤖")

st.title("🤖 Sidad Pro AI")
st.subheader("سیستەمێ ژیریێ دەستکرد ب بادینی")

# 2. Setup Client
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("کلیل (API Key) د ناڤ Secrets دا نینە!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. User Input
if prompt := st.chat_input("سداد، پرسیارا تە چییە؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are Sidad's AI. Speak ONLY in Kurdish Badini dialect (Zakho/Duhok style)."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                stream=True
            )
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Error: {e}")
