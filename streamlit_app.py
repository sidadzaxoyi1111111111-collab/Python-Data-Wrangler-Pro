import streamlit as st
import google.generativeai as genai

# --- [ڕاکێشانا کلیلێ ب ڕێکا ستریملێت] ---
# تێبینی: سداد، ئەڤ کۆدە دێ کلیلێ ژ 'Secrets' یێن تە خوینیت ب بێ دەنگی
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    st.title("🤖 Sidad Data Wrangler Pro")
    st.markdown("---")
    st.write("هەیلا برا سداد! مێشکێ AI نوکە یێ کار دکەت و کلیل یا پاراستی و ڤەشارتییە. 💀🔥")

    # --- [بەشێ پرسیار و بەرسڤێ] ---
    user_input = st.text_input("پرسیارەکێ ب زمانێ کوردی (زاخۆیی) بکە:", placeholder="بێژە من چەوا دێ کارێ خۆ باشتر کەم؟")
    
    if user_input:
        with st.spinner('دێ مێشکێ خۆ گەرم کەم...'):
            try:
                # فەرمان بۆ AI دا ب شێوەزارێ بادینی بەرسڤ بدەت
                prompt = f"بەرسڤا ڤێ بدە ب زمانێ کوردی بادینی (شێوەزارێ زاخۆ): {user_input}"
                response = model.generate_content(prompt)
                st.info(f"✅ بەرسڤا AI: \n\n {response.text}")
            except Exception as e:
                st.error(f"❌ ئاریشەک هەبوو د مێشکی دا! دبیت کلیل یا مرتی بیت.")
else:
    st.error("❌ سداد! کلیل د بەشێ Secrets دا نەهاتییە دیتن.")
    st.info("💡 ل سەر سایتێ ستریملێت، هەرە Settings -> Secrets و کلیلێ ل وێرێ دانیە.")

st.markdown("---")
st.caption("Sidad AI Security Mode: Enabled 🔒")
