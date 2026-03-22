import streamlit as st
import requests

st.title("🔍 Sidad AI - Connection Tester")

# 1. وەرگرتنا کلیلێ
hf_token = st.secrets.get("HF_TOKEN")

if not hf_token:
    st.error("❌ کلیل د Secrets دا نەهاتییە دیتن! کەرەم بکە HF_TOKEN زێدە بکە.")
else:
    st.info(f"🔑 کلیل یێ هەی (دەسپێک: {hf_token[:5]}...)")
    
    # 2. تاقیکرنەکا سادە دگەڵ سێرڤەرێ Hugging Face
    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-1B-Instruct"
    headers = {"Authorization": f"Bearer {hf_token}"}
    
    if st.button("پشکنینێ بکە (Test Connection)"):
        try:
            with st.spinner("یێ تاقی دکەم..."):
                response = requests.post(API_URL, headers=headers, json={"inputs": "Hi"})
                result = response.json()
                
                if response.status_code == 200:
                    st.success("✅ پیرۆزە! کلیلێ تە ١٠٠٪ یێ درستە و کار دکەت.")
                    st.write("بەرسڤا سێرڤەری:", result)
                elif response.status_code == 401:
                    st.error("❌ کلیلێ تە یێ شلەیە (Invalid Token). کەرەم بکە ئێکێ نوو دروست بکە.")
                else:
                    st.warning(f"⚠️ کێشەیەک هەیە. کدێ خەتایێ: {response.status_code}")
                    st.write(result)
        except Exception as e:
            st.error(f"❌ خەتایەک د ئینتەرنێتێ دا هەیە: {e}")

st.sidebar.write("Owner: **Sidad Ahmad**")
