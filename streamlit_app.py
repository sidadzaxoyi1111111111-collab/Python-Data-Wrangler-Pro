import streamlit as st
import requests

# 1. Setup Page
st.set_page_config(page_title="Sidad AI Hero", page_icon="👑")
st.title("👑 Sidad AI - Stable Edition")

# 2. Get Token from Secrets
hf_token = st.secrets.get("HF_TOKEN")

if not hf_token:
    st.error("⚠️ کەرەم بکە کلیلا HF_TOKEN د ناڤ Secrets دا زێدە بکە.")
else:
    if "messages" not in st.session_state:
        st.session_state.messages = []
        welcome = "سلاڤ سداد! ئەڤە وەشانا جێگیر و ب هێز یا **Sidad AI** یە. ئەز نوکە یێ بەرهەڤم!"
        st.session_state.messages.append({"role": "assistant", "content": welcome})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # مۆدێلا Llama 3.1 (عیملاق)
    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-8B-Instruct"
    headers = {"Authorization": f"Bearer {hf_token}"}

    if prompt := st.chat_input("پسیارەکێ ب بادینی بکە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # ڕێنماییا بادینی (Badini Expert Logic)
                payload = {
                    "inputs": f"<|system|>\nYou are Sidad AI, a professional assistant from Zakho. Speak ONLY in Badini Kurdish dialect. Use words like: دکەم, دچم, چەوانی, سوپاس.\n<|user|>\n{prompt}\n<|assistant|>\n",
                    "parameters": {"max_new_tokens": 500, "temperature": 0.7, "return_full_text": False}
                }
                
                response = requests.post(API_URL, headers=headers, json=payload)
                result = response.json()
                
                if isinstance(result, list) and 'generated_text' in result[0]:
                    res_content = result[0]['generated_text']
                    # پاقژکرنا بەرسڤێ ژ تێکستێن زێدە
                    res_content = res_content.split("<|assistant|>")[-1].strip()
                    
                    st.markdown(res_content)
                    st.session_state.messages.append({"role": "assistant", "content": res_content})
                else:
                    st.warning("سێرڤەر یێ دهێتە بارکرن (Loading)، چەند چرکەکێن دی تاقی بکە.")
            except Exception as e:
                st.error(f"Error: {e}")

st.sidebar.write("Owner: **Sidad Ahmad**")
st.sidebar.success("✅ Stable Connection Active")
