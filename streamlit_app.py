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
# تێبینی: مە پەیڤا 'models/' لێکرە ڤە چونکی هندەک سێرڤەر ب بێ وێ قەبوول ناکەن
model_name = 'gemini-1.5-flash'
model = genai.GenerativeModel(model_name)

# ٦. وەرگرتنا رسالێ و بەرسڤدان
user_input = st.chat_input("تشتەکی ب بێژە برا...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Sidad AI یا یێ فکریە..."):
            try:
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([user_input, img])
                else:
                    # مەجبورکرنا بوتێ دا ب بادینی بەرسڤ بدەت
                    full_prompt = f"بەرسڤێ ب زمانێ بادینی بدە: {user_input}"
                    response = model.generate_content(full_prompt)
                
                st.write(response.text)
            except Exception as e:
                # ئەگەر دیسا خەلەتی دا، دێ مۆدێلێ 'gemini-pro' تاقی کەت ئۆتۆماتیکی
                try:
                    model_backup = genai.GenerativeModel('gemini-pro')
                    response = model_backup.generate_content(user_input)
                    st.write(response.text)
                except:
                    st.error(f"سداد برا، خەلەتییەکا تەکنیکی هەیە: {e}")
