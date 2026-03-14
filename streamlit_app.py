import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="Sidad | AI & Engineering Hub", layout="wide")

# Custom CSS for Dark Theme
st.markdown("""
    <style>
    .main { background-color: #0b1e2d; color: white; }
    .stMetric { background-color: #112a40; border: 1px solid #1e3a5f; padding: 20px; border-radius: 12px; }
    h1 { color: #4db8ff; border-bottom: 2px solid #4db8ff; }
    </style>
    """, unsafe_allow_html=True)

# --- SECTION 1: TECHNICAL PROFILE ---
st.title("TECHNICAL ENGINEERING PROFILE 🚀")
col_a, col_b = st.columns([2,1])
with col_a:
    st.write("**Candidate:** Sidad Ahmad | **Expertise:** Python, SQL, AI")
with col_b:
    st.write("**Location:** Zakho / Remote")

# Metrics (Like your image)
c1, c2, c3 = st.columns(3)
c1.metric("API LATENCY", "45ms", "-10ms")
c2.metric("DB THROUGHPUT", "1.2k req/s", "15%")
c3.metric("AI ACCURACY", "98.4%", "0.2%")

st.markdown("---")

# --- SECTION 2: AI CHATBOT INTERFACE ---
st.subheader("💬 AI Assistant (Powered by GPT)")

# Input for API Key (Safety First)
with st.expander("🔐 Configure AI Settings"):
    openai_api_key = st.text_input("OpenAI API Key", type="password")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello Sidad! How can I help you with your data today?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Here you would call OpenAI API - for now, we show a mock response
    response = f"Sidad, this is a simulated response to: {prompt}. (Connect your API key for real AI)"
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
