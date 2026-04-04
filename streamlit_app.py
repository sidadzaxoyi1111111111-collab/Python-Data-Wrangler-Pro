import streamlit as st
import requests
import json

# --- 1. ڕێکخستنا لاپەرەی ---
st.set_page_config(page_title="Sidad AI Pro Agent", page_icon="🤖", layout="centered")

# --- 2. وەرگرتنا کلیلێ ژ Secrets ---
# ل دێشبۆردێ Streamlit د پشکا Secrets دا بنڤێسە: OPENROUTER_API_KEY = "کلیل"
if "OPENROUTER_API_KEY" in st.secrets:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
else:
    st.error("کلیل د Secrets دا نەهاتییە دیتن! تکایە کلیلێ ل دێشبۆردێ Streamlit زێدە بکە.")
    st.stop()

# --- 3. ناڤنیشان و ستایل ---
st.title("🤖 Sidad AI Pro Agent")
st.markdown("---")
st.info("بخێر بێی بۆ بۆتێ من یێ نوی یێ بهێز! ئەڤە پڕۆژێ من یێ پایتۆنە.")

# --- 4. دروستکرنا بیردانکا چاتی (Chat History) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشاندانا نامەیێن کۆن
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. وەرگرتنا نامەیا نوی ژ بەکارهێنەری ---
if prompt := st.chat_input("پسیارا تە چییە سداد؟"):
    # زێدەکرنا نامەیا تە بۆ لیستێ
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- 6. پەیوەندی ب OpenRouter API ---
    with st.chat_message("assistant"):
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://sidad-python-pro.streamlit.app", 
            "X-Title": "Sidad AI Agent"
        }
        
        # مۆدێلێ Mistral 7B Instruct کو نوکە کار دکەت و بێبەرامبەرە
        data = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": st.session_state.messages
        }
        
        try:
            with st.spinner("ل هیڤیا بەرسڤێ بە..."):
                response = requests.post(url, headers=headers, data=json.dumps(data))
                
                if response.status_code == 200:
                    result = response.json()
                    if 'choices' in result and len(result['choices']) > 0:
                        full_response = result['choices'][0]['message']['content']
                        st.markdown(full_response)
                        # پاشکەفتکرنا بەرسڤێ
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    else:
                        st.warning("بەرسڤ هات بەس یا چۆل بوو. سحکە کلیلێ.")
                else:
                    # نیشاندانا ئەڕۆرا سێرڤەری ب ڕوونی
                    st.error(f"Error {response.status_code}")
                    st.json(response.json())
                    
        except Exception as e:
            st.error(f"کێشەیەک د پەیوەندیێ دا هەیه: {e}")

# --- پاشکۆ ---
st.markdown("---")
st.caption("Powered by Sidad Ahmed | Computer Science Graduate")
