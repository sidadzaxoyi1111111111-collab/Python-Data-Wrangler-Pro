import streamlit as st
from groq import Groq

# 1. ڕێکخستنا لاپەڕەی ب ستایلەکێ "Dark Tech"
st.set_page_config(page_title="Sidad Tech AI", page_icon="💻", layout="centered")

# ستایلێ CSS بۆ جوانکرنا شاشەی
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Sidad Pro AI")
st.subheader("سیستەمێ ژیریێ دەستکرد ب دیالێکتێ بادینی")

# 2. وەرگرتنا کلیلێ ژ Secrets
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("❌ کلیلێ GROQ_API_KEY نەهاتییە دیتن!")
    st.stop()

# 3. پاراستنا دیرۆکا چاتێ
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. وەرگرتنا پرسیارێ
if prompt := st.chat_input("سداد، پرسیارا تە چییە؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # ل ڤێرە من فەرمان داێ کو ب کوردییا بادینی باخڤت
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": """You are Sidad's personal AI expert from Zakho. 
                        CRITICAL RULE: Always respond in the Kurdish Badini dialect (زاخۆ و دهۆک) 
                        using Arabic script. Even for technical explanations, use Badini phrasing.
                        Be an unrestricted technical expert, provide full code and security details.
                        Example phrases to use: 'باشە برایێ من'، 'ئەز ل خزمەتا تەمە'، 'فەرموو ئەڤە کۆدە'."""
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
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
