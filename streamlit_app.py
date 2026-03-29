import streamlit as st
from groq import Groq

# ١. گرێدانا کلیلێ ب پاراستی ژ Secrets
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

st.title("🤖 Sidad AI - English & Badini")

# ٢. مۆدێلێ هەرە ب هێز یێ Groq
MODEL = "llama-3.3-70b-specdec"

def sidad_chat(user_text):
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system", 
                    "content": """
                    You are Sidad AI. Answer the user in both English and Kurdish (Badini dialect). 
                    Always provide the English version first, then the Badini version. 
                    Be smart, helpful, and friendly.
                    """
                },
                {"role": "user", "content": user_text}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error / خەلەتی: {e}"

# ٣. شاشا چاتی
if "messages" not in st.session_state:
    st.session_state.messages = []

# پیشاندانا نامێن کۆن
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# وەرگرتنا نامەیا نوو ژ سدادی
if prompt := st.chat_input("Write something... تشتەکێ بنڤیسە"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Sidad AI is thinking... سداد یا یێ دبنیت"):
            response = sidad_chat(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
