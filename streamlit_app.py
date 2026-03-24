import streamlit as st
import google.generativeai as genai

# ڕێکخستنا لاپەری
st.set_page_config(page_title="Sidad AI Wrangler", page_icon="🤖")

# ١. پشکنینا کلیلێ ژ Secrets
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    
    try:
        # ڕێکخستنا API ب ڤێرژنا نوی
        genai.configure(api_key=API_KEY)
        
        # گوهۆرینا ناڤێ مۆدێلی بۆ شێوازێ فەرمی یێ گوگل
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        st.title("🤖 Sidad AI Wrangler")
        st.success("✅ پیرۆزە سداد! نوکە مێشکێ AI یێ گرێدایە.")

        user_input = st.text_input("ب زاخۆیی پرسیارەکێ بکە:")
        
        if user_input:
            with st.spinner('دێ مێشکێ خۆ گەرم کەم...'):
                # فەرمان بۆ AI ب زمانێ کوردی بادینی
                prompt = f"بەرسڤا ڤێ بدە ب زمانێ کوردی بادینی (شێوەزارێ زاخۆ): {user_input}"
                response = model.generate_content(prompt)
                
                if response.text:
                    st.info(f"✅ AI دبیژیت: \n\n {response.text}")
                else:
                    st.warning("⚠️ بەرسڤ نەهات، دبیت کێشەک د ئینتەرنێتێ دا هەبیت.")
                    
    except Exception as e:
        # ئەگەر دیسان خەلەتی دا، دێ ل ڤێرێ نیشا تە دەت
        st.error(f"❌ ئاریشە: {str(e)}")
else:
    st.error("❌ سداد! کلیل د بەشێ Secrets دا نەهاتییە دیتن.")

st.markdown("---")
st.caption("Sidad AI - Final Fix Mode 🚀")
