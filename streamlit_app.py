import streamlit as st
import google.generativeai as genai
from PIL import Image

# ١. ڕێکخستنا لاپەرەی بۆ "Sidad AI Agent"
st.set_page_config(page_title="Sidad AI Agent", page_icon="🤖", layout="centered")

# ٢. دیزاینێ سەرەکی یێ سایتێ سداد
st.markdown("""
<div style="background-color: #0c1a2c; padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #1f3a5f;">
    <h1 style="color: white; margin-bottom: 0;">🤖 Sidad AI Agent</h1>
    <p style="color: #6c99cb; font-size: 18px; direction: rtl;">سڵاو سداد برا، ئەز ل خزمەتا تە دام ب زمانێ بادینی ۆو ئینگلیزی.</p>
</div>
