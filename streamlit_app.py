import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# ١. ناڤ و نیشانێ سایتێ سداد (مۆبایلا Infinix Pro Note 50)
st.set_page_config(page_title="Sidad AI Agent", page_icon="🤖", layout="centered")

# ٢. دیزاینێ جوان و نڤیسینا بادینی
st.markdown("""
<div style="background-color: #0c1a2c; padding: 25px; border-radius: 20px; border: 1px solid #1f3a5f; margin-bottom: 25px;">
    <h1 style="color: white; text-align: center; font-size: 38px; margin-bottom: 5px;">🤖 Sidad AI Agent</h1>
    <p style="color: #6c99cb; text-align: center; font-size: 19px; margin-top: 0; direction: rtl;">
    سڵاو سداد برا، ئەز ل خزمەتا تە دام ب زمانێ بادینی ۆو ئینگلیزییا فول.
    </p>
</div>
""", unsafe_allow_html=True)

# ٣. ڕێکخستنا کلیلێ API و وێنەی ل Sidebar
with st.sidebar:
    st.title("🛠️ تنظیمات")
    api_key = st.text_input("کلیلێ Gemini API ل ڤێرە دانی برا:", type="password")
    st.markdown("---")
    uploaded_file = st.file_uploader("وێنەیەکێ هەڵبژێرە (JPG, PNG)...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        st.image(uploaded_file, caption='وێنێ تە یێ ئامادەیە', use_column_width=True)
    
    st.info("سداد، تو ٢٥ سالی و داتا سپێشالیستی. ئەڤ بوتە یێ پاراستییە.")

# ٤. کاراکردنا مێشکێ Gemini
if api_key:
    genai.configure(api_key=api_
