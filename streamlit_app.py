import streamlit as st
from g4f.client import Client

# 1. Setup Page
st.set_page_config(page_title="Sidad AI Pro", page_icon="🛡️")
st.title("🛡️ Sidad AI - Pro Edition")

# 2. History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Smart Provider Logic
# ل ڤێرە 'Client' دێ کار کەت چونکی مە ل سەری 'Import' کرییە
client = Client()

if prompt := st.chat_input("سلاڤەکێ ب بادینی بکە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # ڕێنماییا بادینی
            instruction = "STRICT: Answer in Badini Kurdish dialect only. "
            
            response = client.chat.completions.create(
                model="gpt-4o", 
                messages=[
                    {"role": "system", "content": "You are Sidad AI, created by Sidad Ahmad. Speak Badini."},
                    {"role": "user", "content": instruction + prompt}
                ]
            )
            res = response.choices[0].message.content
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        except:
            st.error("سێرڤەر مژوولە، کێمەکێ دی تاقی بکە.")

st.sidebar.write("Owner: **Sidad Ahmad**")
st.sidebar.success("✅ Fixed NameError")
