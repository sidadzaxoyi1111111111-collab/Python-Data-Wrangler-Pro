import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Sidad AI", page_icon="🤖")
st.title("🤖 Sidad AI")
st.divider()

api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction="تۆ چاتبۆتێکی زیرەکی. بادینی، کوردی، ئینگلیزی، عەرەبی دەزانیت. بە زمانی بەکارهێنەر وەڵام بدەرەوە."
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if st.button("🗑️ پاككردن"):
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])
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
            try:
                response = st.session_state.chat.send_message(prompt)
                reply = response.text
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"کێشەیەک هەیە: {str(e)}")
