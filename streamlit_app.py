import streamlit as st

# Setup page style
st.set_page_config(page_title="Sidad Tech Profile", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b1e2d; color: white; }
    .stMetric { background-color: #112a40; border: 1px solid #1e3a5f; padding: 20px; border-radius: 12px; }
    h1 { color: #4db8ff; border-bottom: 2px solid #4db8ff; }
    .footer-bar { background-color: #081621; padding: 10px; border-radius: 8px; text-align: center; color: #4db8ff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Header (Matching your image)
st.title("TECHNICAL ENGINEERING PROFILE 🚀")
col_info1, col_info2 = st.columns([2,1])
with col_info1:
    st.write("**Candidate:** Sidad Ahmad")
    st.write("**Expertise:** Python (FastAPI, Async), SQL, AI Integration")
with col_info2:
    st.write("**Location:** Zakho / Remote")

st.markdown("<h2 style='text-align: center; color: #4db8ff;'>高性能 Data & AI Dashboard 💻</h2>", unsafe_allow_html=True)

# Metrics Section
col1, col2, col3 = st.columns(3)
col1.metric("API LATENCY", "45ms", "-10ms")
col2.metric("DB THROUGHPUT", "1.2k req/s", "15%")
col3.metric("AI ACCURACY", "98.4%", "0.2%")

st.markdown('<div class="footer-bar">📊 System Load Analysis 📊</div>', unsafe_allow_html=True)
st.caption("<p style='text-align: center;'>Dashboard is Live and Fully Functional.</p>", unsafe_allow_html=True)
