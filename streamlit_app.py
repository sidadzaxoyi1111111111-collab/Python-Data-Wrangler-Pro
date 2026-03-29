import streamlit as st
import google.generativeai as genai
from PIL import Image

# ١. ڕێکخستنا لاپەرەی
st.set_page_config(page_title="Sidad AI Agent", layout="centered")

# ٢. ناڤ و نیشانێ سایتێ سداد
st.title("🤖 Sidad AI Agent")
st.write("سڵاو سداد برا، ئەز ل خزمەتا تە دام ب زمانێ بادینی ۆو ئینگلیزی.")

# ٣. خویندنا کلیلێ ژ Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("سداد، کلیل د ناڤ Secrets دا نینە!")
    st.stop()

# ٤. Sidebar بۆ وێنەیان
with st.sidebar:
    st.header("📸 وێنە دابەزینە")
    uploaded_file = st.file_uploader("وێنەیەکێ هەڵبژێرە...", type=["jpg", "png", "jpeg"])

# ٥. مێشکێ Gemini (Flash Model)
model = genai.GenerativeModel('gemini-1.5-flash')

# ٦. وەرگرتنا رسالێ و بەرسڤدان
user_input = st.chat_input("تشتەکی ب بێژە برا...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        try:
            if uploaded_file:
                img = Image.open(uploaded_file)
                response = model.generate_content([user_input, img])
            else:
                response = model.generate_content(user_input)
            st.write(response.text)
        except Exception as e:
            st.error(f"خەلەتییەک چێ بوو: {e}")
