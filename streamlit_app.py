import streamlit as st
from google import genai

# کلیلێن تە یێن تایبەت (Gemini Key)
GEMINI_KEY = 'AIzaSyCHpLbDrdwt8QDB5e-n7aZBvaTh0pwZws4'

# ڕێکخستنا لاپەرێ وێبێ
st.set_page_config(page_title="Sidad AI Dashboard", page_icon="🤖")

st.title("🤖 Sidad AI - Gemini 2.0 Interface")
st.markdown("ئەڤە ناوبەستەکێ وێبێ یە بۆ تاقیکرنا مۆدێلا ژیریا دەستکرد ب زمانی کوردی بادینی.")

# لایێ چەپێ یێ شاشێ (Sidebar)
with st.sidebar:
    st.header("Settings")
    model_name = st.selectbox("Select Model", ["gemini-2.0-flash", "gemini-1.5-flash"])
    st.info("Built by Sidad Ahmad | Python Developer")

# شوونا چاتێ (Chat Interface)
if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشادانا نامەیێن کۆن
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# وەرگرتنا نامێ ژ بەکارهێنەری
if prompt := st.chat_input("چی ل مێشکێ تە دایە؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # پەیوەندی ل گەل Gemini API ب کلیلێن تە
    try:
        client = genai.Client(api_key=GEMINI_KEY)
        with st.chat_message("assistant"):
            response = client.models.generate_content(
                model=model_name,
                contents=f"تۆ یاریدەدەرێکی زیرەکی، بە زمانی کوردی بادینی وەڵامی سیداد بدەوە: {prompt}"
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")
