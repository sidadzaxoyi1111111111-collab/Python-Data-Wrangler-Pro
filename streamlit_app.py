import streamlit as st
from groq import Groq

# 1. Setup
st.set_page_config(page_title="Sidad AI", page_icon="🤖")
st.title("🤖 Sidad AI (Ultra Fast)")

# 2. API Key
api_key = st.secrets.get("GEMINI_KEY")

if not api_key:
    st.error("⚠️ کلیل ل ناڤ Secrets نەهاتییە دیتن!")
else:
    client = Groq(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("پسیارەکێ بکە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # بکارئینانا مۆدێلا Llama 3.3 یا زۆر ب لەز
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "تۆ Sidad AI، ب زمانی کوردی بادینی بەرسڤێ بدە."},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                response_text = chat_completion.choices[0].message.content
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Error: {e}")
