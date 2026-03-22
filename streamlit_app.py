import streamlit as st
import google.generativeai as genai

# 1. Setup
st.set_page_config(page_title="Sidad AI Fix", page_icon="🔧")
st.title("🔧 Sidad AI - Connection Fix")

api_key = st.secrets.get("GEMINI_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # تاقیکرنا مۆدێلێ ب شێوەیەکێ دروست
        # ناڤێ مۆدێلێ ب ڤی ڕەنگی بنڤیسە: models/gemini-1.5-flash
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        if "chat" not in st.session_state:
            st.session_state.chat = model.start_chat(history=[])

        if prompt := st.chat_input("سلاڤەکێ بکە..."):
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                # فرێکرنا نامەیێ
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
                
    except Exception as e:
        # ئەگەر خەتایەک هەبیت ل ڤێرە دێ نیشا تە دەت
        st.error(f"Detailed Error: {e}")
else:
    st.warning("Please add GEMINI_KEY to Streamlit Secrets.")

st.sidebar.write("Owner: **Sidad Ahmad**")
