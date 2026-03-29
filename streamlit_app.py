import streamlit as st
import google.generativeai as genai

# ١. خویندنا کلیلا ڤەشارتی ژ Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # ٢. دروستکرنا مۆدێلێ Gemini
    system_instruction = "ناڤێ تە Sidad AI Agent یە. تو ب بادینی دئاخڤی و ئینگلیزییا تە فولە."
    model = genai.GenerativeModel('gemini-1.5-pro-latest', system_instruction=system_instruction)
    
except KeyError:
    st.error("سداد برا، من کلیل نەدیت! دڵنیابە تە ناڤێ وێ کرییە GEMINI_API_KEY د ناڤ Secrets دا.")
    st.stop()

# ٣. ل ڤێرە تو دشێی "Request" فرێکەی
user_input = st.chat_input("تشتەکی ب بێژە برا...")

if user_input:
    with st.chat_message("assistant"):
        response = model.generate_content(user_input)
        st.write(response.text)
