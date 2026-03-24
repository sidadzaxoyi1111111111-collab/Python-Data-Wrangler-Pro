import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Sidad AI Wrangler", page_icon="🤖")

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    st.title("🤖 Sidad AI Wrangler")
    
    # لیستا مۆدێلێن دبیت کار بکەن
    model_names = ['gemini-1.5-flash', 'gemini-1.0-pro', 'gemini-pro']
    
    user_input = st.text_input("ب زاخۆیی پرسیارەکێ بکە (بۆ نموونە: سڵاو):")
    
    if user_input:
        with st.spinner('دێ مێشکێ خۆ گەرم کەم...'):
            success = False
            for m_name in model_names:
                try:
                    model = genai.GenerativeModel(m_name)
                    prompt = f"بەرسڤا ڤێ بدە ب زمانێ کوردی بادینی (شێوەزارێ زاخۆ): {user_input}"
                    response = model.generate_content(prompt)
                    
                    st.success(f"✅ (Model: {m_name})")
                    st.info(f"🤖 AI دبیژیت: \n\n {response.text}")
                    success = True
                    break # ئەگەر کار کر، دێ ڕاوەستیت
                except Exception:
                    continue # ئەگەر کار نەکر، دێ چیتە سەر یێ دی
            
            if not success:
                st.error("❌ سداد برا، چو مۆدێل ل سەر ڤێ کلیلێ کار ناکەن. دبیت کێشە د 'Region' یان 'Version' دا هەبیت.")
else:
    st.error("❌ کلیل نەهاتییە دیتن د Secrets دا!")

st.markdown("---")
st.caption("Sidad AI - Smart Version Selector 🚀")
