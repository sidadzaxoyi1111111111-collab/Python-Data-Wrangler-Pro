import streamlit as st
import requests
import json

# --- 1. ڕێکخستنا لاپەرەی ---
st.set_page_config(page_title="Sidad AI Pro Agent", page_icon="🤖", layout="centered")

# --- 2. وەرگرتنا کلیلێ ژ Secrets ---
if "GROQ_API_KEY" in st.secrets:
    API_KEY = st.secrets["GROQ_API_KEY"]
else:
    st.error("کلیل د Secrets دا نەهاتییە دیتن! تکایە کلیلێ ب ناڤێ GROQ_API_KEY زێدە بکە.")
    st.stop()

# --- 3. دیزاینا دەرڤە ---
st.title("🤖 Sidad AI Pro Agent")
st.markdown("---")
st.info("بخێر بێی بۆ بۆتێ من یێ نوی! ئەڤە پڕۆژێ منە کو ب تەکنۆلۆژییا Groq کار دکەت.")

# --- 4. دروستکرنا بیردانکا چاتی ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشاندانا نامەیێن کۆن
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. وەرگرتنا نامەیا نوی ---
if prompt := st.chat_input("پسیارا تە چییە سداد؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- 6. پەیوەندی ب Groq API ---
    with st.chat_message("assistant"):
        # لینکا فەرمی یا Groq بۆ مۆدێلێن وەک Llama
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama-3.3-70b-versatile", # مۆدێلێ هەرە بهێز و بەلاش یێ Groq
            "messages": st.session_state.messages
        }
        
        try:
            with st.spinner("ل هیڤیا بەرسڤێ بە..."):
                response = requests.post(url, headers=headers, data=json.dumps(data))
                
                if response.status_code == 200:
                    result = response.json()
                    full_response = result['choices'][0]['message']['content']
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.error(f"Error {response.status_code}")
                    st.json(response.json())
                    
        except Exception as e:
            st.error(f"کێشەیەک د پەیوەندیێ دا هەیه: {e}")

# --- پاشکۆ ---
st.markdown("---")
st.caption("Developed by Sidad Ahmed | Powered by Groq Cloud")
