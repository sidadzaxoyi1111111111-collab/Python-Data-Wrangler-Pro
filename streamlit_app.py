import streamlit as st
import os

st.set_page_config(page_title="Sidad AI Chat", page_icon="💬")
st.title("Sidad AI - Crypto Chat 🚀")

# --- دروستکرنا فۆڵدەرێ هەلگرتنا نامەیان (وەکی مێژوویا چاتی) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- نیشاندانا نامەیێن کۆن (وەکی واتساپ) ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- جهێ نڤیسینا نامەیا نوی (Chat Input) ---
if prompt := st.chat_input("نامەیا خۆ لێرە بنڤیسە..."):
    # 1. نیشاندانا نامەیا تە
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. وەڵاما بوتێ تە (ل ڤێرە بوت دێ بەرسڤێ دەت)
    response = f"سداد برا، نامەیا تە گەهشت: {prompt}. ئەز نوکە تەماشەی بازاڕی دکەم..."
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# --- نیشاندانا وێنەی (ئەگەر هەبیت) ---
st.sidebar.subheader("📊 چارتێ بازاڕی")
if os.path.exists("chart.png"):
    st.sidebar.image("chart.png", caption="SOL/USDT")
else:
    st.sidebar.warning("وێنەیێ chart.png ل سەر GitHub نینە.")
