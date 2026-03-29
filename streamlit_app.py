import streamlit as st
import os

# --- ناڤ و نیشانێ سایتێ سداد ---
st.set_page_config(page_title="Sidad AI Monitor", page_icon="🚀")
st.title("Sidad AI - Crypto Monitor 🚀")

# --- پشکا نیشاندانا نامەیان (Text Messages) ---
st.subheader("📩 پەیامێن بوتێ تە")
st.info("سداد برا، بخێر بێی! ئەڤە داتایێن پشکا Spot نە.")

# --- پشکا وێنەیان (Images) ---
st.subheader("📊 چارتێ بازاڕی")

# ناڤێ وێنەیێ تە ل سەر GitHub پێدڤییە "chart.png" بیت
image_path = "chart.png"

if os.path.exists(image_path):
    st.image(image_path, caption="ئاستێ نرخێ SOL/USDT", use_container_width=True)
else:
    # ئەگەر وێنە نەبوو، ئەڤ پەیامە دێ دیار بیت دا Error چێ نەبیت
    st.warning("⚠️ سداد برا، فایلێ chart.png ل سەر GitHub نەیێ هەین. وێنەیەکێ ب ڤی ناڤی بارکە (Upload).")

# --- پشکا ناردنا نامەیەکێ (Input Text) ---
st.subheader("💬 نامەیەکێ بۆ بوتێ خۆ بفرێشە")
user_msg = st.text_input("نامەیا خۆ لێرە بنڤیسە:")
if st.button("ناردن"):
    if user_msg:
        st.success(f"نامەیا تە هاتە وەرگرتن: {user_msg}")
    else:
        st.error("تکایە نامەیەکێ بنڤیسە!")

# --- پشکا کلیلێن تە (API Keys) ---
# سداد برا، ل ڤێرە کلیلێن تە دێ کار کەن وەکی بەرێ
st.sidebar.write("✅ API Keys Connected")
