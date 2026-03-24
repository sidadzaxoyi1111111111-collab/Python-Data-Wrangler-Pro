import streamlit as st
from openai import OpenAI

# --- [ ڕێکخستنا لاپەری ] ---
st.set_page_config(page_title="Sidad AI Wrangler", page_icon="🤖")

# --- [ وەرگرتنا کلیلێ ب شێوەیەکێ پاراستی ] ---
if "DEEPSEEK_API_KEY" in st.secrets:
    try:
        # گرێدان ب سێرڤەرێ فەرمی یێ DeepSeek
        client = OpenAI(
            api_key=st.secrets["DEEPSEEK_API_KEY"],
            base_url="https://api.deepseek.com" 
        )
        
        st.title("🤖 Sidad AI Wrangler (DeepSeek V3.2)")
        st.success("✅ کلیل یا گرێدایە! نوکە مێشکێ صینی یێ کار دکەت.")

        user_input = st.text_input("پرسیارەکێ ب زاخۆیی بکە (بۆ نموونە: ئەز کێم؟):")
        
        if user_input:
            with st.spinner('دێ مێشکێ خۆ گەرم کەم...'):
                # بکارئینانا مۆدێلێ چاتێ یێ زیرەک
                response = client.chat.completions.create(
                    model="deepseek-chat", # ئەڤە مۆدێلێ گشتی یێ زیرەکە
                    messages=[
                        {"role": "system", "content": "بەرسڤێ ب کوردی بادینی شێوەزارێ زاخۆ بدە."},
                        {"role": "user", "content": user_input}
                    ]
                )
                
                answer = response.choices[0].message.content
                st.info(f"✅ AI دبیژیت: \n\n {answer}")
                
    except Exception as e:
        st.error(f"❌ ئاریشە: {str(e)}")
else:
    st.error("❌ سداد! کلیل د Secrets دا نەهاتییە دیتن.")
