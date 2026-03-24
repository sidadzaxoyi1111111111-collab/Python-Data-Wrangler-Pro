import streamlit as st
import google.generativeai as genai

# ناڤ و نیشانێن لاپەری
st.set_page_config(page_title="Sidad Debugger", page_icon="🔍")

st.title("🤖 Sidad Debugger Mode")

# ١. پشکنینا هەبوونا کلیلێ د Secrets دا
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    
    try:
        # ٢. ڕێکخستنا مۆدێلی
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.success("✅ کلیل د Secrets دا هاتە دیتن.")
        
        user_input = st.text_input("تێستەکێ بکە (بنڤێسە سڵاو):")
        
        if user_input:
            # ٣. هەوڵدان بۆ وەرگرتنا بەرسڤێ
            response = model.generate_content(user_input)
            st.write(f"🤖 AI دبیژیت: {response.text}")
            
    except Exception as e:
        # ⚠️ ل ڤێرێ دێ ناما خەلەتیێ یا دروست نیشا تە دەت
        st.error(f"❌ ئاریشە یا هەی! گوگل دبێژیت: \n\n `{str(e)}` ")
        st.info("سداد برا، ئەگەر نڤێسیبوو 'API key not valid'، رامانا وێ ئەوە کلیل یا سۆتییە.")
else:
    st.error("❌ سداد! کلیل د بەشێ Secrets دا نەهاتییە دیتن. هەرە Settings و دانیە.")

st.markdown("---")
st.caption("Sidad Debugging Mode 🛠️")
