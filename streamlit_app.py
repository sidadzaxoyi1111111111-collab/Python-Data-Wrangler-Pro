import streamlit as st

# Setup page
st.set_page_config(page_title="Sidad Tech Profile", layout="wide")

# Custom UI Styling
st.markdown("""
    <style>
    .main { background-color: #0b1e2d; }
    .stMetric { background-color: #112a40; border: 1px solid #1e3a5f; padding: 20px; border-radius: 12px; color: white; }
    h1 { color: #4db8ff; border-bottom: 2px solid #4db8ff; padding-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Profile Header
st.title("TECHNICAL ENGINEERING PROFILE 🚀")
st.write(f"**Candidate:** Sidad Ahmad | **Expertise:** Python, Ruby, SQL | **Location:** Zakho")

st.markdown("---")
st.subheader("高性能 Data & Systems Dashboard 💻")

# Metrics like your image
col1, col2, col3 = st.columns(3)
col1.metric("PYTHON LATENCY", "45ms", "-10ms")
col2.metric("RUBY THROUGHPUT", "1.2k req/s", "15%")
col3.metric("DATA ACCURACY", "98.4%", "0.2%")

st.info("📊 System Status: All services are running and stable.")
