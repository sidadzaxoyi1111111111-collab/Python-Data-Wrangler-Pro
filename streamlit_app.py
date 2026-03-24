import streamlit as st
from openai import OpenAI

# وەرگرتنا کلیلێ ژ Secrets
if "DEEPSEEK_API_KEY" in st.secrets:
    client = OpenAI(
        api_key=st.secrets["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com"
    )
    
    st.title("🤖 Sidad AI Wrangler")
    st.success("✅ کلیل یا کار دکەت!")
    
    user_input = st.text_input("ب زاخۆیی پرسیارەکێ بکە:")
    if user_input:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": user_input}]
        )
        st.write(response.choices[0].message.content)
