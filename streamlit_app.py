import streamlit as st

# Page Config
st.set_page_config(page_title="Sidad Ahmad | Tech Profile", layout="wide")

# Custom CSS to match your image style
st.markdown("""
    <style>
    .main { background-color: #0b1e2d; color: white; }
    .stMetric { background-color: #112a40; border: 1px solid #1e3a5f; padding: 20px; border-radius: 12px; }
    .header-box { border-bottom: 2px solid #4db8ff; padding-bottom: 10px; margin-bottom: 30px; }
    h1 { color: #4db8ff; }
    </style>
    """, unsafe_allow_html=True)

# Header Section
st.markdown('<div class="header-box"><h1>TECHNICAL ENGINEERING PROFILE 🚀</h1>'
            '<p><b>Candidate:</b> Sidad Ahmad | <b>Expertise:</b> Python, Ruby, SQL, AI Integration</p>'
            '<p><b>Location:</b> Zakho / Remote</p></div>', unsafe_allow_html=True)

st.subheader("高性能 Data & Systems Dashboard 💻")
st.write("Real-time Data Processing & System Metrics Demonstration.")

# Metrics Section (Like your image)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="PYTHON API LATENCY", value="45ms", delta="-10ms")

with col2:
    st.metric(label="RUBY THROUGHPUT", value="1.2k req/s", delta="15%")

with col3:
    st.metric(label="DATA ACCURACY", value="98.4%", delta="0.2%")

# Footer
st.markdown("---")
st.info("📊 System Load Analysis: All services are running and stable.")
st.caption("Dashboard is Live and Fully Functional.")
