import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Sidad AI Pro", page_icon="🤖")

# ١. ڕاکێشانا کلیلێ
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    st.title("🤖 Sidad AI Wrangler")
    st.success("✅ کلیل یا چالاکە!")

    # ٢. بکارئینانا مۆدێلێ Gemini Pro (کو پتر دهێتە قەبوول کرن)
    try:
        model = genai.GenerativeModel('gemini-pro') 
        
        user_input = st.text_input("پرسیارەکێ ب زمانێ کوردی (زاخۆیی) بکە:")
        
        if user_input:
            with st.spinner('دێ مێشکێ خۆ گەرم کەم...'):
                prompt = f"بەرسڤا ڤێ بدە ب زمانێ کوردی بادینی (شێوەزارێ زاخۆ): {user_input}"
                response = model.generate_content(prompt)
                st.info(f"✅ AI دبیژیت: \n\n {response.text}")
                
    except Exception as e:
        # ئەگەر دیسان 404 دا، دێ ڤێرژنەکا دی تاقی کەین
        st.error(f"❌ ئاریشەک هەبوو: {str(e)}")
        st.info("سداد برا، ئەگەر هەر 404 دا، بێژە من دا مۆدێلێ 'gemini-1.0-pro' تاقی بکەین.")
else:
    st.error("❌ کلیل نەهاتییە دیتن د Secrets دا!")

st.markdown("---")
st.caption("Sidad AI - Optimized for Gemini Pro 🚀")
