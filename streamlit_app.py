import streamlit as st
import google.generativeai as genai

# ١. پشتڕاستکرنا کلیلێ
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("سداد، کلیل د ناڤ Secrets دا نینە!")
    st.stop()

# ٢. بکارئینانا مۆدێلێ 'gemini-1.5-flash'
# ئەڤە مسۆگەرترین ناڤە کو 404 نادەت
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # ٣. تاقیکرنەکا سادە (Request)
    user_input = st.chat_input("سلاف، تو کار دکەی؟")
    
    if user_input:
        response = model.generate_content(f"بەرسڤێ ب بادینی بدە: {user_input}")
        st.write(response.text)
        
except Exception as e:
    st.error(f"سداد برا، دیسا خەلەتی دا: {e}")
