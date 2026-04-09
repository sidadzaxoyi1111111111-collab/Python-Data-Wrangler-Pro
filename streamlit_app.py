من کۆدەکەت دەبینم! تۆ بۆتێک دروست کردوە کە زمانی کوردی (بەدینی) بەکاردەهێنێت. ئەگەر دەتەوێت بۆتەکە **تەنها زمانی ئینگلیزی** بەکاربھێنێت و زمانی کوردی جیابکاتەوە، دەتوانم کۆدەکەت بۆت بگۆڕم:

```python
import streamlit as st
import requests
import json

# --- 1. Page Configuration ---
st.set_page_config(page_title="Sidad AI English Assistant", page_icon="🤖", layout="wide")

# --- 2. Get API Key from Secrets ---
if "GROQ_API_KEY" in st.secrets:
    API_KEY = st.secrets["GROQ_API_KEY"]
else:
    st.error("Error: GROQ_API_KEY not found in Secrets!")
    st.stop()

# --- 3. Sidebar for Profile ---
with st.sidebar:
    st.title("👨‍💻 Developer Profile")
    st.markdown(f"**Name:** Sidad Ahmed")
    st.markdown(f"**Field:** Computer Science Graduate")
    st.markdown(f"**Specialist:** Python & CyberSec")
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 Sidad AI - English Assistant")
st.caption("Professional | Technical | English Only")

# --- 4. Create Chat Memory ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. Get New Message ---
if prompt := st.chat_input("Ask me anything in English..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        # --- SYSTEM PROMPT: Changed to English only ---
        system_instruction = (
            "You are Sidad AI Assistant, an expert in Python programming, cybersecurity, and technical fields. "
            "Your master is Sidad Ahmed. You are a professional AI assistant specialized in: "
            "1. Python programming and scripting "
            "2. Cybersecurity concepts and tools "
            "3. Linux system administration "
            "4. Technical problem-solving "
            "CRITICAL INSTRUCTIONS: "
            "- Speak ONLY in English. Never use Kurdish or any other language. "
            "- Be direct, technical, and professional. "
            "- If asked for code, scripts, or technical solutions, provide them clearly. "
            "- Maintain a professional tone at all times. "
            "- Use technical terminology appropriately. "
            "- Format code properly with explanations. "
            "Remember: You are an English-only technical assistant."
        )

        messages_to_send = [{"role": "system", "content": system_instruction}] + st.session_state.messages

        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": messages_to_send,
            "temperature": 0.7,  # Slightly lower for more professional responses
            "max_tokens": 4096
        }
        
        try:
            with st.spinner("Processing..."):
                response = requests.post(url, headers=headers, data=json.dumps(data))
                
                if response.status_code == 200:
                    result = response.json()
                    full_response = result['choices'][0]['message']['content']
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.error(f"API Error {response.status_code}")
                    st.json(response.json())
                    
        except Exception as e:
            st.error(f"Connection Failed: {e}")

st.markdown("---")
st.caption("Property of Sidad Ahmed © 2026 | English AI Assistant")
```

**گۆڕانکارییە سەرەکییەکان:**
1. **سیستەم پرۆمپت**: گۆڕدراوە بۆ تەنها زمانی ئینگلیزی
2. **تیترەکان**: گۆڕدراون بۆ ئینگلیزی
3. **ڕەفتار**: پیشەییتر و تەکنیکیترە
4. **پلەی گەرمی**: کەمکراوەتەوە بۆ ٠.٧ بۆ وەڵامی ڕێکتر
5. **دەستپێشخەری چات**: گۆڕدراوە بۆ "Ask me anything in English..."

**ئەگەر دەتەوێت:**
- **ھەردو زمان بەکاربھێنێت** (ئینگلیزی و کوردی)
- **بە پێی دەستکاری بڕیار بدات** کە چ زمانێک بەکاربھێنێت
- **تایبەتمەندییەکی تری زیاد بکەیت**

بڵێیت، دەتوانم کۆدەکە بۆت زیادەڕۆیتر بکەم!
