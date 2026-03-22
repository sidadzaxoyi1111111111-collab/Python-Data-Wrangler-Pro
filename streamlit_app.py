import streamlit as st
import requests
import time

# 1. Setup Page
st.set_page_config(page_title="Sidad AI King", page_icon="👑")
st.title("👑 Sidad AI - Turbo Edition")

# 2. Get Token from Secrets
hf_token = st.secrets.get("HF_TOKEN")

if not hf_token:
    st.error("⚠️ کەرەم بکە کلیلا HF_TOKEN د ناڤ Secrets دا زێدە بکە.")
else:
    if "messages" not in st.session_state:
        st.session_state.messages = []
        welcome = "سلاڤ سداد! ئەڤە وەشانا **Turbo** یا Sidad AI یە. ئەز نوکە گەلەک یێ خێرام!"
        st.session_state.messages.append({"role": "assistant", "content": welcome})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # مۆدێلا Qwen 2.5 (گەلەک یا خێرا و زیرەکە)
    API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-72B-Instruct"
    headers = {"Authorization": f"Bearer {hf_token}"}

    if prompt := st.chat_input("پسیارەکێ ب بادینی بکە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("یێ دگەڕێم..."):
                try:
                    payload = {
                        "inputs": f"<|im_start|>system\nYou are Sidad AI. Speak ONLY in Badini Kurdish dialect.<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n",
                        "parameters": {"max_new_tokens": 512, "temperature": 0.7}
                    }
                    
                    response = requests.post(API_URL, headers=headers, json=payload)
                    result = response.json()
                    
                    # ئەگەر مۆدێل یێ دهێتە بارکرن، دێ پەیامەکا جوان دەت
                    if "error" in result and "currently loading" in result["error"]:
                        st.warning("⏳ مۆدێل یێ هشیار دبیتەڤە، هیڤییە ١٠ چرکەیان چاڤەڕێ بە و دیسا بنڤیسە.")
                    else:
                        res_content = result[0]['generated_text'].split("<|im_start|>assistant\n")[-1].strip()
                        st.markdown(res_content)
                        st.session_state.messages.append({"role": "assistant", "content": res_content})
                except:
                    st.error("سێرڤەر یێ مژوولە، کێمەکێ دی تاقی بکە.")

st.sidebar.write("Owner: **Sidad Ahmad**")
st.sidebar.success("🚀 Turbo Mode Active")
