import streamlit as st
from PIL import Image

# ١. زێدەکرنا بەشێ دابەزاندنا وێنەی ل لایێ چەپێ (Sidebar)
with st.sidebar:
    st.title("📸 ناڤەندێ وێنەیان")
    uploaded_file = st.file_uploader("وێنەیەکێ هەڵبژێرە برا...", type=["jpg", "png", "jpeg"])

# ٢. ئەگەر وێنە هاتە هەڵبژاردن، دێ ل ناڤ چاتی دیار بیت
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='وێنێ تە یێ هاتییە دابەزاندن', use_column_width=True)
    
    # ل ڤێرە تو دشێی وێنەی بدەیە Gemini دا شەرح بکەت
    st.info("سداد، وێنە هاتە دابەزاندن! نوکە ل خوارێ پرسیارا خۆ ل سەر بکە.")
