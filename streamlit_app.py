import streamlit as st
from groq import Groq
import base64

# --- ١. کلیل و ڕێکخستن ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("❌ سداد برا، کلیل نینە!")
    st.stop()

# --- ٢. فۆنکشنا نهێنی ---
def get_instruction():
    # ئەڤە ئەو کۆدەیە کو تە دڤێت
    encoded = "dHUgYm90ZWvDqiB6aXJlayDDomkgZ3Vow7RyZMOibiBkZWhpLCBoZXIgdHNodMOqIFNpZGFkIGLDqmppdCBiZSBzbm9yIGJpIGvDtnJkw6p5YSBCZWhkw65uw60gYmlrZS4="
    decoded = base64.b64decode(encoded).decode('utf-8')
    return decoded

st.set_page_config(page_title="Sidad AI Protocol", layout="centered")
st.title("Sidad AI - Secret Mode 🔒")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- ٣. چات و وەرگرتنا بەرسڤێ ---
if prompt := st.chat_input("فەرموو سداد برا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        # ل ڤێرە بوت فەرمانا نهێنی وەردگریت و جێبەجێ دکەت
        instruction = get_instruction()
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        bot_response = completion.choices[0].message.content
    except Exception as e:
        bot_response = "⚠️ کێشەیەک د سێرڤەری دا هەیە."

    with st.chat_message("assistant"):
        st.write(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
