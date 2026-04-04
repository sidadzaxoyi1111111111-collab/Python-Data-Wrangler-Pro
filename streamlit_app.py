import streamlit as st
import requests
import json

# --- ڕێکخستنا لاپەرەی ---
st.set_page_config(page_title="Sidad AI Pro Agent", page_icon="🤖", layout="centered")

# --- وەرگرتنا کلیلێ ژ Secrets ---
# پشتڕاست بە کو د Streamlit Cloud دا ناڤێ کلیلێ یێ دروستە
if "OPENROUTER_API_KEY" in st.secrets:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
else:
    st.error("کلیل د Secrets دا نەهاتییە دیتن! کلیلێ ل دێشبۆردێ Streamlit زێدە بکە.")
    st.stop()

# --- ستایلێ دەرڤە ---
st.title("🤖 Sidad AI Pro Agent")
st.markdown("---")
st.info("بخێر بێی بۆ بۆتێ من یێ نوی یێ بهێز! ئەڤە پڕۆژێ من یێ پایتۆنە.")

# --- دروستکرنا بیردانکا چاتی (Chat History) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشاندانا نامەیێن کۆن
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- وەرگرتنا نامەیا نوی ژ بەکارهێنەری ---
if prompt := st.chat_input("پسیارا تە چییە؟"):
    # زێدەکرنا نامەیا بەکارهێنەری بۆ لیستێ
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- پەیوەندی ب OpenRouter API ---
    with st.chat_message("assistant"):
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://sidad-python-pro.streamlit.app", # ناڤێ سایتێ تە
            "X-Title": "Sidad AI Agent"
        }
        
        data = {
            "model": "google/gemini-2.0-flash-exp:free", # مۆدێلەکێ بێبەرامبەر و جێگیر
            "messages": st.session_state.messages
        }
        
        try:
            with st.spinner("ل هیڤیا بەرسڤێ بە..."):
                response = requests.post(url, headers=headers, data=json.dumps(data))
                
                if response.status_code == 200:
                    result = response.json()
                    full_response = result['choices'][0]['message']['content']
                    st.markdown(full_response)
                    # پاشکەفتکرنا بەرسڤێ
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
                    
        except Exception as e:
            st.error(f"کێشەیەک د پەیوەندیێ دا هەیه: {e}")

# --- پاشکۆ ---
st.markdown("---")
st.caption("Powered by Sidad Ahmed | Python & AI Specialist")
