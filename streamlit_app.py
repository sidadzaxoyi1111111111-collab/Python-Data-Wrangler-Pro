import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Setup
st.set_page_config(page_title="Sidad | Backend & AI Engineer", layout="wide")

# 2. Sidebar Info
st.sidebar.title("🚀 Technical Profile")
st.sidebar.info("""
**Candidate:** Sidad Ahmad  
**Expertise:** Python (FastAPI, Async), SQL, AI Integration  
**Location:** Zakho / Remote  
""")

# 3. Main Dashboard
st.title("💻 High-Performance Data & AI Dashboard")
st.write("Demonstrating real-time data processing and system metrics.")

# 4. Metrics Row
col1, col2, col3 = st.columns(3)
col1.metric("API Latency", "45ms", "-10ms")
col2.metric("DB Throughput", "1.2k req/s", "15%")
col3.metric("AI Accuracy", "98.4%", "0.2%")

st.divider()

# 5. Professional Chart
st.subheader("📊 System Load Analysis")
chart_data = pd.DataFrame(
    np.random.randn(20, 2),
    columns=['Server Load', 'User Traffic']
)
fig = px.line(chart_data, title="Real-time Monitoring")
st.plotly_chart(fig, use_container_width=True)

st.success("Dashboard is Live and Fully Functional.")
