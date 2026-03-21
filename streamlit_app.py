import streamlit as st
from google import genai
import os

# وەرگرتنا کلیلان ب شێوەیەکێ پاراستی (Environment Variables)
# ئەڤە ناهێلیت کلیلێن تە ئاشکرا ببن و بلۆک ببن
GEMINI_KEY = os.getenv('GEMINI_KEY')

# ڕێکخستنا لاپەرێ وێبێ
st.set_page_config(page_title="Sidad AI Dashboard", page_icon="🤖")

st.title("🤖 Sidad AI - Gemini 2.0 Interface")
st.markdown("ئەڤە ناوبەستەکێ وێبێ یە بۆ تاقیکرنا مۆدێلا ژیریا دەستکرد ب زمانی کوردی بادینی.")

# لایێ چەپێ یێ شاشێ (Sidebar)
with st.sidebar:
    st.header("Settings")
    model_name = st.selectbox("Select Model", ["gemini-2.0-flash", "gemini-1.5-flash"])
    st.divider()
    st.info("Built by Sidad Ahmad | Python Developer")

# شوونا چاتێ (Chat Interface)
if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشادانا نامەیێن کۆن
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# وەرگرتنا نامێ ژ بەکارهێنەری
if prompt := st.chat_input("چی ل م
