import streamlit as st
import requests

# 1. Setup Page
st.set_page_config(page_title="Sidad AI Fixed", page_icon="🚀")
st.title("🚀 Sidad AI - Final Version")

# 2. Get Token from Secrets
hf_token = st.secrets.get("HF_TOKEN")

if not hf_token:
    st.error("❌ کەرەم بکە کلیلا HF_TOKEN د ناڤ Secrets دا زێدە بکە.")
else:
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": "سلاڤ سداد! ئەڤە وەشانا نوو و جێگیرە. ئەز یێ بەرهەڤم."})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ئەڤە ئەو لینکێ نوویە یێ Hugging Face داخواز کری (Router API)
    API_URL = "https://router.huggingface.co/hf-inference/models/meta-llama/Llama-3.2-3B-Instruct"
    headers = {"Authorization": f"Bearer {hf_token}"}

    if prompt := st.chat_input("پسیارەکێ ب بادینی بکە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                payload = {
                    "model": "meta-llama/Llama-3.2-3B-Instruct",
                    "messages": [
                        {"role": "system", "content": "You are Sidad AI. Answer only in Badini Kurdish dialect."},
                        {"role": "user", "content": prompt}
                    ],
                    "parameters": {"max_new_tokens": 500}
                }
                
                response = requests.post(API_URL, headers=headers, json=payload)
                result = response.json()
                
                # وەرگرتنا بەرسڤێ ب شێوەیەکێ درست
                if "choices" in result:
                    res_content = result['choices'][0]['message']['content']
                    st.markdown(res_content)
                    st.session_state.messages.append({"role": "assistant", "content": res_content})
                elif "error" in result:
                    st.warning(f"⚠️ سێرڤەر دبێژیت: {result['error']}")
                else:
                    st.error("ئاریشەکا نەدیار هەبوو، دیسا تاقی بکە.")
            except Exception as e:
                st.error(f"❌ Error: {e}")

st.sidebar.write("Owner: **Sidad Ahmad**")
st.sidebar.success("✅ Router API Active")
