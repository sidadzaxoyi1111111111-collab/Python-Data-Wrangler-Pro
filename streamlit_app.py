import streamlit as st
import google.generativeai as genai

# 1. ڕێکخستنا لاپەڕەی
st.set_page_config(page_title="Sidad AI Pro", page_icon="🤖", layout="centered")
st.title("🤖 Sidad AI - Professional Edition")
st.markdown("---")

# 2. وەرگرتنا کلیلێ ژ سێکرێتس
api_key = st.secrets.get("GEMINI_KEY")

if not api_key:
    st.error("⚠️ کلیل د سێکرێتس دا نەهاتییە دیتن! کەرەم بکە GEMINI_KEY زێدە بکە.")
else:
    # ڕێکخستنا مۆدێلا گوگل
    genai.configure(api_key=api_key)
    
    # ڕێنماییا مێشکێ بادینی (Strict Badini Rules)
    badini_logic = (
        "You are Sidad AI, a professional assistant from Zakho. Creator: Sidad Ahmad.\n"
        "STRICT LANGUAGE RULES:\n"
        "- Speak ONLY in Badini Kurdish (Kurmanji dialect).\n"
        "- Use words: 'دکەم', 'دچم', 'دڤێت', 'چەوانی', 'سوپاس', 'کەرەم بکە'.\n"
        "- DO NOT use Sorani words like 'دەکەم', 'دەچم', 'یارمەتی'.\n"
        "If the user speaks English, respond in professional academic English."
    )

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=badini_logic
    )

    # دەسپێکرنا چاتێ
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # نیشاندانا نامەیێن پێشتر
    for message in st.session_state.chat_session.history:
        role = "assistant" if message.role == "model" else "user"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

    # پسیارەکا نوو
    if prompt := st.chat_input("پسیارەکێ ب بادینی بکە..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                response = st.session_state.chat_session.send_message(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")

# سایدبار بۆ زانیارییان
st.sidebar.markdown("---")
st.sidebar.write("Owner: **Sidad Ahmad**")
st.sidebar.write("Engine: **Gemini 1.5 Flash**")
st.sidebar.success("✅ System Online")
