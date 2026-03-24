import streamlit as st
from openai import OpenAI

# ڕێکخستنا لاپەری
st.set_page_config(page_title="Sidad AI Wrangler", page_icon="💀")

if "DEEPSEEK_API_KEY" in st.secrets:
    try:
        # ل ڤێرێ پێدڤییە base_url یێ دروست بیت
        # ئەگەر تو DeepSeek بکاربینی: https://api.deepseek.com
        # ئەگەر تو سایتەکێ دی یێ مۆدێلان بکاربینی، لینکێ وان دانیە
        client = OpenAI(
            api_key=st.secrets["DEEPSEEK_API_KEY"],
            base_url="https://api.deepseek.com" 
        )
        
        st.title("🤖 Sidad AI Wrangler")
        st.success("✅ کلیل یا گرێدایە!")

        user_input = st.text_input("ب زاخۆیی پرسیارەکێ بکە:")
        
        if user_input:
            with st.spinner('دێ مێشکێ خۆ گەرم کەم...'):
                response = client.chat.completions.create(
                    model="deepseek-chat", # یان "deepseek-reasoner"
                    messages=[
                        {"role": "system", "content": "بەرسڤێ ب کوردی بادینی شێوەزارێ زاخۆ بدە."},
                        {"role": "user", "content": user_input}
                    ]
                )
                st.info(f"✅ AI دبیژیت: \n\n {response.choices[0].message.content}")
                
    except Exception as e:
        st.error(f"❌ ئاریشە د ناسنامێ دا (Auth Error): \n\n `{str(e)}` ")
        st.info("سداد برا، ئەگەر نڤێسیبوو 'Insufficient Balance'، رامانا وێ ئەوە پێدڤی ب پارەیە.")
else:
    st.error("❌ کلیل د Secrets دا نەهاتییە دیتن!")
