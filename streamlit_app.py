import streamlit as st
import google.generativeai as genai
from PIL import Image

# ١. ڕێکخستنا لاپەرەی بۆ سداد
st.set_page_config(page_title="Sidad AI Agent", page_icon="🤖")

# ٢. خویندنا کلیلێ ب شێوەیەکێ پاراستی ژ Secrets
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("سداد برا، کلیل د ناڤ Secrets دا نینە! ناڤێ وێ بکە: GEMINI_API_KEY")
    st.stop()

# ٣. دیزاینێ سەرەکی
st.title("🤖 Sidad AI Agent")
st.write("سڵاو سداد برا، ئەز ل خزمەتا تە دام ب زمانێ بادینی.")

# ٤. Sidebar بۆ وێنەیان
with st.sidebar:
    st.header("📸 وێنە دابەزینە")
    uploaded_file = st.file_uploader("وێنەیەکێ هەڵبژێرە...", type=["jpg", "png", "jpeg"])
    st.info("سداد، تو ٢٥ سالی و ل زاخۆ یی. ئەڤ بوتە یێ پاراستییە.")

# ٥. ئەڤە دێ کێشەیا 404 چارەسەر کەت (بکارئینانا ناڤێ سادە)
# تێبینی: مە ناڤ کورت کر دا کو ب دروستی کار بکت
model = genai.GenerativeModel('gemini-pro')

# ٦. وەرگرتنا رسالێ و بەرسڤدان
user_input = st.chat_input("تشتەکی ب بێژە برا...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Sidad AI یا یێ فکریە..."):
            try:
                # تاقی کرن ب مۆدێلێ جێگیر 'gemini-pro'
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    # ئەگەر وێنە هەبیت، دێ مۆدێلێ 'gemini-1.5-flash' بکار ئینیت
                    vision_model = genai.GenerativeModel('gemini-1.5-flash')
                    response = vision_model.generate_content([user_input, img])
                else:
                    # ئەگەر بتنێ دەق بیت، دێ مۆدێلێ 'gemini-pro' بکار ئینیت
                    full_prompt = f"بەرسڤێ ب زمانێ بادینی بدە: {user_input}"
                    response = model.generate_content(full_prompt)
                
                st.write(response.text)
            except Exception as e:
                st.error(f"سداد برا، خەلەتییەکا تەکنیکی هەیە: {e}")
