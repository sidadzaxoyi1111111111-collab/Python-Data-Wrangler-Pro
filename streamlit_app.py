import streamlit as st
import google.generativeai as genai

# 1. ڕێکخستنا لاپەڕەی
st.set_page_config(page_title="Sidad AI", page_icon="🤖", layout="centered")
st.title("🤖 Sidad AI - Gemini 1.5 Flash")
st.markdown("---")

# 2. ئینان و پشتڕاستکرنا کلیلێ (API Key)
api_key = st.secrets.get("GEMINI_KEY")

if not api_key:
    st.error("⚠️ خەتا: کلیل (API Key) د ناڤ Secrets دا نەهاتییە دیتن!")
    st.info("بچۆ ناڤ Settings > Secrets و کلیلێ ل وێرێ دانێ.")
else:
    # ڕێکخستنا گوگل ئەی ئای
    genai.configure(api_key=api_key)
    
    # ناساندنا مۆدێلێ ب شێوەیەکێ گشتی دا خەتایا 404 نەمینیت
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 3. پاراستنا دیرۆکا چاتی (Chat History)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # نیشاندانا نامەیێن کۆن
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 4. وەرگرتنا نامەیا نوی ژ بەکارهێنەری
    if prompt := st.chat_input("پسیارەکێ بکە..."):
        # زێدەکرنا نامەیا تە بۆ لیستی
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # بەرسڤدان ب ڕێکا Gemini
        with st.chat_message("assistant"):
            try:
                # فەرمان دناڤبەرا کۆدی دا بۆ زمانێ بادینی
                system_prompt = f"تۆ یاریدەدەره‌كێ زیرەکی ب ناڤێ Sidad AI، ب تنێ ب زمانی کوردی بادینی بەرسڤێ بدە: {prompt}"
                
                response = model.generate_content(system_prompt)
                
                if
