import streamlit as st
import google.generativeai as genai

# ١. لێرە کلیل ب ڕەنگەکێ ڕاستەوخۆ هاتییە دانان (پێدڤی ب سیکرێتس نینە)
GEMINI_KEY = "AIzaSyD_xIP9De8bCQiT8f_LDajtpV8vi7N62hI"
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ٢. دیزاینا سایتێ سداد
st.set_page_config(page_title="Sidad AI Dashboard", page_icon="🤖")
st.title("🤖 Sidad AI Dashboard")

# ٣. لۆجیکێ چاتێ
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تشتەکێ بنڤیسە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # ناردنا نامێ بۆ Gemini
            full_prompt = f"بەرسڤ بدە ب کوردی بادینی: {prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"ئاریشەیەک هەبوو: {str(e)}")
