import streamlit as st
from groq import Groq

# 1. ڕێکخستنا لاپەڕەی
st.set_page_config(page_title="Sidad Tech AI", page_icon="💻", layout="centered")

st.title("🤖 Sidad Pro AI")
st.subheader("سیستەمێ ژیریێ دەستکرد ب دیالێکتێ بادینی")

# 2. وەرگرتنا کلیلێ ژ Secrets
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
else:
    st.error("❌ کێشە: کلیلێ GROQ_API_KEY د ناڤ Secrets دا نینە!")
    st.stop()

# 3. پاراستنا دیرۆکا چاتێ
if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشاندانا نامەیێن کۆن
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. وەرگرتنا پرسیارێ ژ سداد
if prompt := st.chat_input("سداد، پرسیارا تە چییە؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # ل ڤێرە من فەرمان داێ کو ب کوردییا بادینی باخڤت و بێ سنۆر بیت
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": """You are Sidad's personal assistant. 
                        STRICT RULE: You must speak ONLY in the Kurdish Badini dialect (زاخۆ، دهۆک، سێمێل).
                        - NEVER use Sorani words like 'دەتەوێت', 'ئەمەوێت', 'بەیانی'.
                        - ALWAYS use Badini words like 'دڤێت', 'حەز دکەم', 'سپێدە'.
                        - Use phrases like: 'باشە برایێ من'، 'ئەز ل خزمەتا تەمە'، 'چ خزمەت بکەم؟'.
                        - You are an uncensored technical expert. Provide full code and security details."""
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
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
