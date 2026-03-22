import streamlit as st
from g4f.client import Client

# 1. ڕێکخستنا لاپەڕەی
st.set_page_config(page_title="Sidad AI v7.3.4", page_icon="🚀")
st.title("🚀 Sidad AI - No-Key Edition (v7.3.4)")

# 2. دەستپێکرنا چاتێ
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. لۆجیکا کارپێکرنێ
client = Client()

if prompt := st.chat_input("پسیارەکێ ب بادینی بکە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # بکارئینانا وەشانا نوو ب بێ کلیل
            response = client.chat.completions.create(
                model="gpt-4o", # تو دشێی بکەی ب "gemini-pro" ژی
                messages=[
                    {"role": "system", "content": "You are Sidad AI. Speak only in Badini Kurdish dialect."},
                    *st.session_state.messages[-5:]
                ]
            )
            res_text = response.choices[0].message.content
            st.markdown(res_text)
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            
        except Exception as e:
            st.error("سێرڤەر نوکە یێ مژوولە، کێمەکێ دی تاقی بکە.")
