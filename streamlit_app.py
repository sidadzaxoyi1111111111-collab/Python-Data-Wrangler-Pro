import streamlit as st
import requests

# --- ١. پشکنینا کلیلێ د Secrets دا ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ سداد برا، کلیل د بەشێ Secrets دا نینە! ل سەر ئێک دێڕ دانی.")
    st.stop()

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# --- ٢. دێزاینا سایتێ سداد ---
st.set_page_config(page_title="Sidad AI Portal", page_icon="🐲")
st.title("🐲 Sidad AI Agent")
st.markdown("ئەڤە سیستەمێ تە یێ ژیرە کو ب مێشکێ **Llama 3.3** کار دکەت.")

# --- ٣. فۆنکشنا پەیوەندیێ ب Groq ڤە ---
def ask_groq(user_query):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "ناڤێ تە Sidad AI یە و تو ب بادینی بەرسڤێ ددەی."},
            {"role": "user", "content": user_query}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"❌ خەتایا Groq: {response.json().get('error', {}).get('message', 'نەدیار')}"
    except Exception as e:
        return f"❌ کێشە د پەیوەندیێ دا: {str(e)}"

# --- ٤. لۆژیکێ چاتێ (Chat Interface) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# پیشاندانا نامەیێن کۆن
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# وەرگرتنا نامەیا نوو ژ سدادی
if prompt := st.chat_input("تشتەکێ بنڤیسە سداد برا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("یێ دهزریت..."):
            response = ask_groq(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
