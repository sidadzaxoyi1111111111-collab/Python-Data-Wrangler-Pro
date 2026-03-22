import streamlit as st
import google.generativeai as genai

# 1. ڕێکخستنا لاپەڕەی
st.set_page_config(page_title="Sidad AI Fixed", page_icon="🤖")
st.title("🤖 Sidad AI - Connection Fixed")

# 2. وەرگرتنا کلیلێ
api_key = st.secrets.get("GEMINI_KEY")

if not api_key:
    st.error("⚠️ کلیل د Secrets دا نەهاتییە دیتن!")
else:
    try:
        genai.configure(api_key=api_key)
        
        # چارەسەریا فەرمی بۆ خەتایا 404:
        # بکارئینانا 'gemini-1.5-flash-latest' ل شوونا ناڤێ کۆن
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        if "chat_session" not in st.session_state:
            # ڕێنماییا مێشکێ بادینی
            badini_logic = "You are Sidad AI. Speak ONLY in Badini Kurdish dialect. Be professional."
            st.session_state.chat_session = model.start_chat(history=[])

        # نیشاندانا نامەیێن کۆن
        for message in st.session_state.chat_session.history:
            role = "assistant" if message.role == "model" else "user"
            with st.chat_message(role):
                st.markdown(message.parts[0].text)

        # چاتا نوو
        if prompt := st.chat_input("سلاڤەکێ ب بادینی بکە..."):
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                try:
                    # فرێکرنا نامەیێ
                    response = st.session_state.chat_session.send_message(prompt)
                    st.markdown(response.text)
                except Exception as inner_e:
                    st.error(f"Google Response Error: {inner_e}")
                
    except Exception as e:
        st.error(f"Connection Error: {e}")

st.sidebar.markdown("---")
st.sidebar.write("Owner: **Sidad Ahmad**")
st.sidebar.info("Engine: **Gemini 1.5 Flash Latest**")
