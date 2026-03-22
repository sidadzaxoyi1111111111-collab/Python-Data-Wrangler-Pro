import streamlit as st
from openai import OpenAI

st.title("🚀 Sidad AI - GPT-4o Edition")

# وەرگرتنا کلیلێ
api_key = st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ کەرەم بکە کلیلێ د Secrets دا زێدە بکە.")
else:
    client = OpenAI(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("پسیارەکێ ب بادینی بکە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are Sidad AI. Speak ONLY in Badini Kurdish dialect."},
                        *st.session_state.messages
                    ]
                )
                res = response.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except Exception as e:
                st.error(f"Error: {e}")
