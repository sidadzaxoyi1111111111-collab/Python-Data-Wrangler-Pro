import streamlit as st
import google.generativeai as genai
from PIL import Image

# ١. ڕێکخستنا لاپەرەی بۆ سداد
st.set_page_config(page_title="Sidad AI Agent", page_icon="🤖")

# ٢. خویندنا کلیلێ ب شێوەیەکێ پاراستی
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("سداد برا، کلیل د ناڤ Secrets دا نینە!")
    st.stop()

# ٣. دیزاینێ سەرەکی
st.title("🤖 Sidad AI Agent")
st.write("سڵاو سداد برا، ئەز ل خزمەتا تە دام ب زمانێ بادینی.")

# ٤. Sidebar بۆ وێنەیان
with st.sidebar:
    st.header("📸 وێنە دابەزینە")
    uploaded_file = st.file_uploader("وێنەیەکێ هەڵبژێرە...", type=["jpg", "png", "jpeg"])
    st.info("سداد، تو ٢٥ سالی و ل زاخۆ یی. ئەڤ بوتە یێ پاراستییە.")

# ٥. بەکارهێنانا مۆدێلێ Stable (ئەڤە خەلەتییا 404 نادەت)
# ل ڤێرە مە ناڤ کورت کر دا کو ب دروستی کار بکت
model = genai.GenerativeModel('gemini-1.5-flash')

# ٦. وەرگرتنا رسالێ
user_input = st.chat_input("تشتەکی ب بێژە برا...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        try:
            if uploaded_file:
                img = Image.open(uploaded_file)
                # ناردنا وێنە و دەقی ب پێکڤە
                response = model.generate_content([user_input, img])
            else:
                # ناردنا دەقی بتنێ ب زمانێ بادینی
                full_prompt = f"بەرسڤێ ب زمانێ بادینی بدە: {user_input}"
                response = model.generate_content(full_prompt)
            
            st.write(response.text)
        except Exception as e:
            st.error(f"خەلەتییەک چێ بوو: {e}")
