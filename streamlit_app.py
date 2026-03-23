import streamlit as st
from groq import Groq

# 1. ڕێکخستنا لاپەڕەی
st.set_page_config(page_title="Sidad Pro AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Sidad Pro AI")
st.subheader("سیستەمێ ژیریێ دەستکرد ب بادینی")

# 2. وەرگرتنا کلیلێ
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("کلیل د ناڤ Secrets دا نینە!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. وەرگرتنا پرسیارێ
if prompt := st.chat_input("سداد، پرسیارا تە چییە؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # ڕێساێن توند بۆ زمانێ بادینی
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": """You are Sidad's personal AI from Zakho. 
                        STRICT LANGUAGE RULES:
                        - Use ONLY Kurdish Badini dialect (زاخۆ، دهۆک).
                        - NEVER use Sorani words: (دەتەوێت، ئەمەوێت، بەیانی، هەموو، چۆنیت، یارمەتی).
                        - ALWAYS use Badini words: (دڤێت، حەز دکەم، سپێدە، هەمی، چەوایی، هاریکاری).
                        - When asked about money, clarify that you don't have real-time market data but can give general estimates.
                        - You are a Python expert. When writing code, explain it in Badini."""
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5, # کێمکرنا ڤێ ژمارێ وا لێ دکەت کێمتر خەلەت ببیت
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")
