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

# 3. Intelligent Switching Logic
client = Client()

if prompt := st.chat_input("سلاڤەکێ ب بادینی بکە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # لیستەکا سێرڤەرێن کو زۆرترین جاران کار دکەن
        providers = [
            g4f.Provider.Blackbox,
            g4f.Provider.ChatGptEs,
            g4f.Provider.DuckDuckGo,
            g4f.Provider.Liaobots
        ]
        
        success = False
        for provider in providers:
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    provider=provider,
                    messages=[
                        {"role": "system", "content": "You are Sidad AI. Creator: Sidad Ahmad. Speak Badini Kurdish ONLY."},
                        {"role": "user", "content": prompt}
                    ]
                )
                res = response.choices[0].message.content
                if res and len(res) > 2:
                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})
                    success = True
                    break
            except:
                continue # ئەگەر یێ ئێکێ مژوول بوو، دێ چیتە سەر یێ دووێ
        
        if not success:
            st.error("هەمی سێرڤەر مژوولن! هیڤییە ١٠ چرکێن دی تاقی بکەڤە.")

st.sidebar.write("Owner: **Sidad Ahmad**")
st.sidebar.info("🚀 Using Multi-Provider Logic")
