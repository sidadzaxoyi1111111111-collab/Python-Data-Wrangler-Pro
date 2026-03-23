import anthropic
import streamlit as st

st.set_page_config(page_title="Sidad AI", page_icon="🤖")
st.title("🤖 Sidad AI")
st.divider()

api_key = st.secrets["ANTHROPIC_API_KEY"]
client = anthropic.Anthropic(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("🗑️ پاككردن"):
    st.session_state.messages = []
    st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("پرسیارەکەت بنووسە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("چاوەڕێ بکە..."):
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                system="تۆ چاتبۆتێکی زیرەکی. بادینی، کوردی، ئینگلیزی، عەرەبی دەزانیت. بە زمانی بەکارهێنەر وەڵام بدەرەوە.",
                messages=st.session_state.messages
            )
            reply = response.content[0].text
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
