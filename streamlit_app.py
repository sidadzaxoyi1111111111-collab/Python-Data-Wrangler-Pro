import streamlit as st

# 1. Page Configuration (Dark Theme Style)
st.set_page_config(page_title="Sidad Ahmad | Tech Profile", layout="wide")

# 2. Custom CSS to match your image exactly
st.markdown("""
    <style>
    .main { background-color: #0b1e2d; color: white; }
    .stMetric { 
        background-color: #112a40; 
        border: 1px solid #1e3a5f; 
        padding: 20px; 
        border-radius: 12px; 
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .header-box { 
        border-bottom: 2px solid #4db8ff; 
        padding-bottom: 10px; 
        margin-bottom: 30px; 
    }
    h1 { color: #4db8ff; font-family: 'Segoe UI', sans-serif; }
    .footer-bar {
        background-color: #081621;
        border: 1px solid #1e3a5f;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        color: #4db8ff;
        font-weight: bold;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Section (Matching your image)
st.markdown('<div class="header-box">', unsafe_allow_html=True)
col_title, col_details = st.columns([2, 1])

with col_title:
    st.title("TECHNICAL ENGINEERING PROFILE 🚀")

with col_details:
    st.markdown("""
    **Candidate:** Sidad Ahmad  
    **Expertise:** Python (FastAPI, Async), SQL, AI  
    **Location:** Zakho / Remote
    """)
st.markdown('</div>', unsafe_allow_html=True)

# 4. Dashboard Section
st.markdown("<h2 style='text-align: center; color: #4db8ff;'>高性能 Data & AI Dashboard 💻</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Real-time Data Processing & System Metrics Demonstration.</p>", unsafe_allow_html=True)

# 5. Metrics Grid (API, DB, AI)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="API LATENCY", value="45ms", delta="-10ms")

with col2:
    st.metric(label="DB THROUGHPUT", value="1.2k req/s", delta="15%")

with col3:
    st.metric(label="AI ACCURACY", value="98.4%", delta="0.2%")

# 6. System Load Bar (Footer of the dashboard)
st.markdown('<div class="footer-bar">📊 System Load Analysis 📊</div>', unsafe_allow_html=True)

st.write("")
st.markdown("<p style='text-align: center; color: #566573;'>Dashboard is Live and Fully Functional.</p>", unsafe_allow_html=True)
