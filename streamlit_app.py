import streamlit as st
import g4f
from g4f.client import Client

# 1. Setup Page
st.set_page_config(page_title="Sidad AI Pro", page_icon="👑")
st.title("👑 Sidad AI - Pro Edition")

# 2. History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Intelligent Logic (Auto-Provider)
client = Client()

if prompt := st.chat_input("سلاڤەکێ ب بادینی بکە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # ل ڤێرە مە 'provider' کرە ئۆتۆماتیک دا تووشی 'AttributeError' نەبی
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are Sidad AI. Answer in Badini Kurdish dialect only. Creator: Sidad Ahmad."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            res = response.choices[0].message.content
            if res:
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            else:
                st.error("بەرسڤ یا چۆل بوو، دیسا تاقی بکە.")
                
        except Exception as e:
            st.error("سێرڤەرێن بێ کلیل نوکە یێن مژوولن. هیڤییە کێمەکێ دی تاقی بکە.")

st.sidebar.write("Owner: **Sidad Ahmad**")
st.sidebar.success("✅ Auto-Provider Active")
