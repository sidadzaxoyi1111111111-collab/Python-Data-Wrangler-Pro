import streamlit as st
import google.generativeai as genai

# 1. Setup Page
st.set_page_config(page_title="Sidad AI Pro", page_icon="🤖")
st.title("🤖 Sidad AI - The Ultimate Fix")

# 2. Get API Key
api_key = st.secrets.get("GEMINI_KEY")

if not api_key:
    st.error("⚠️ کلیل د Secrets دا نینە!")
else:
    try:
        genai.configure(api_key=api_key)
        
        # گوهۆڕینا ستراتیژییەتێ: بکارئینانا gemini-pro کو ل هەمی ڤێرژنان کار دکەت
        # ئەڤە دێ خەتایا 404 نەهێلیت
        model = genai.GenerativeModel('gemini-pro')

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # نیشاندانا نامەیان
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # چاتێ نوو
        if prompt := st.chat_input("سلاڤەکێ بکە..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                try:
                    # ڕێنماییا بادینی د ناڤ بەرسڤێ دا
                    instruction = "بەرسڤێ ب تەمامی ب زمانی بادینی بدە و بێژە ئەز Sidad AI مە. "
                    full_prompt = instruction + prompt
                    
                    response = model.generate_content(full_prompt)
                    res_text = response.text
                    
                    st.markdown(res_text)
                    st.session_state.chat_history.append({"role": "assistant", "content": res_text})
                except Exception as inner_e:
                    st.error(f"Error: {inner_e}")
                    
    except Exception as e:
        st.error(f"Connection Error: {e}")

st.sidebar.write("Owner: **Sidad Ahmad**")
st.sidebar.info("Engine: **Gemini Pro Stable**")
