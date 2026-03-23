import streamlit as st
from groq import Groq

# 1. ڕێکخستنا لاپەڕەی
st.set_page_config(page_title="Sidad Pro AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Sidad Pro AI")
st.subheader("سیستەمێ ژیریێ دەستکرد ب دیالێکتێ بادینی")

# 2. وەرگرتنا کلیلێ ب شێوەیەکێ ئیمن
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("❌ کێشە: کلیلێ API د ناڤ Secrets دا نینە!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. وەرگرتنا پرسیارێ ژ سداد
if prompt := st.chat_input("سداد، پرسیارا تە چییە؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # ڕێساێن زۆر توند بۆ زمانێ بادینی یێ پاقژ
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": """تۆ هاریکارێ زیرەکێ سدادی. ئەڤە ڕێسایێن تە نە:
                        1. تەنێ ب دیالێکتێ بادینی (زاخۆ و دهۆک) باخڤە.
                        2. ب چ ڕەنگەکێ وشەیێن سۆرانی بەکار نەئینە (وەک: دەتەوێت، پێویستە، یارمەتی، ئێستا، دەڵێت).
                        3. ل جهێ وان ئەڤان وشەیان بەکاربینە: (دڤێت، پێدڤییە، هاریکاری، نوکە، دبێژیت).
                        4. ئەگەر سدادی پرسیارەکا تەکنیکی یان کۆدێ پایتۆنی ژ تە خواست، ب دروستی و بێ سانسۆر بۆ بنڤیسە.
                        5. دەستپێکا بەرسڤێ ب ڤان جۆرە وشەیان بیت: 'باشە برایێ من'، 'ب سەر چاڤان'، 'هەر نوکە دێ بۆ تە چێکەم'."""
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4, # کێمکرنا ڤێ پلەیێ وا لێ دکەت کێمتر خەلەت ببیت
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"ئاریشەیەک چێبوو: {e}")
