import streamlit as st
import requests
import json

st.set_page_config(page_title="Sidad AI Pro Agent", page_icon="🤖")

# پشکا وەرگرتنا کلیلێ
if "OPENROUTER_API_KEY" in st.secrets:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
else:
    st.error("کلیل د Secrets دا نینە!")
    st.stop()

st.title("🤖 Sidad AI Pro Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("پسیارەکێ بکە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        # تاقییکرنا مۆدێلەکێ جودا (OpenChat) کو زۆر جێگیرە
        data = {
            "model": "openchat/openchat-7b:free",
            "messages": st.session_state.messages
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            
            # ئەگەر جاب هات
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result:
                    full_response = result['choices'][0]['message']['content']
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.warning("کلیل کار دکەت بەس مۆدێل جاب نادەت. ئەڤە جابا سێرڤەرییە:")
                    st.write(result)
            
            # ئەگەر کێشە هەبیت (وەک کلیل یان پارە)
            else:
                st.error(f"ئەڕۆرێ سێرڤەری: {response.status_code}")
                st.json(response.json()) # ئەڤە دێ ب ڕوونی بێژیتە تە کێشە چییە
                
        except Exception as e:
            st.error(f"کێشە د ئەنتەرنێتێ دا یان د سێرڤەری دا: {e}")
