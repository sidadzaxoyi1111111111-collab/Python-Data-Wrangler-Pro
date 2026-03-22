import streamlit as st
import google.generativeai as genai

# 1. Setup Page
st.set_page_config(page_title="Sidad AI Pro", page_icon="🤖")
st.title("🤖 Sidad AI - Connection Fixed")

# 2. API Key from Secrets
api_key = st.secrets.get("GEMINI_KEY")

if not api_key:
    st.error("⚠️ کلیل د Secrets دا نەهاتییە دیتن!")
else:
    try:
        genai.configure(api_key=api_key)
        
        # چارەسەریا خەتایا 404: بکارئینانا ناڤێ سادە یێ مۆدێلێ
        # ئەگەر 1.5-flash کار نەکر، دێ gemini-pro تاقی کەت
        try:
            model_name = "gemini-1.5-flash"
            model = genai.GenerativeModel(model_name)
        except:
            model_name = "gemini-pro"
            model = genai.GenerativeModel(model_name)

        if "chat_session" not in st.session_state:
            # ڕێنماییا بادینی (Badini Logic)
            sys_msg = "You are Sidad AI. Speak ONLY in Badini Kurdish dialect. Be professional."
            st.session_state.chat_session = model.start_chat(history=[])

        # نیشاندانا نامەیێن کۆن
        for message in st.session_state.chat_session.history:
            role = "assistant" if message.role == "model" else "user"
            with st.chat_message(role):
                st.markdown(message.parts[0].text)

        # چاتێ نوو
        if prompt := st.chat_input("سلاڤەکێ ب بادینی بکە..."):
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                # فرێکرنا نامەیێ ب شێوەیەکێ پاراستی
                response = st.session_state.chat_session.send_message(prompt)
                st.markdown(response.text)
                
    except Exception as e:
        st.error(f"❌ کێشەیەکا نوو هەبوو: {e}")

st.sidebar.markdown("---")
st.sidebar.write("Owner: **Sidad Ahmad**")
st.sidebar.info(f"Active Model: {model_name if 'model_name' in locals() else 'None'}")
