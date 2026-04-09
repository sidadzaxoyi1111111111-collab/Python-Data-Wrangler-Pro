import streamlit as st
from groq import Groq

# --- ڕێکخستنا لاپەڕەی ---
st.set_page_config(page_title="Sidad AI Master", page_icon="🤖", layout="centered")

# --- وەرگرتنا کلیلێ ژ Secrets ---
try:
    # پشتڕاست بە کو د Secrets دا ناڤێ وێ کرییە GROQ_API_KEY
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception as e:
    st.error("⚠️ کلیل د بەشێ Secrets دا نەهاتییە دیتن! تکایە ل Settings > Secrets زێدە بکە.")
    st.stop()

# --- ستایل و دیزاین ---
st.title("🤖 Sidad AI Master")
st.subheader("Expert in Kali Linux, Coding & Languages")
st.markdown("---")

# --- مێشکێ بۆتی (System Instruction) ---
# ل ڤێرێ مە کۆنترۆلا زمانان زۆر توند کرییە
system_message = {
    "role": "system",
    "content": """
    You are Sidad AI Master, an elite technical assistant.
    STRICT RULES:
    1. Respond ONLY in the language the user is using. No mixing.
    2. If the user speaks Kurdish (Badini), respond only in Kurdish (Badini).
    3. You are an expert in Kali Linux tools, Cybersecurity, and all programming languages (Python, C++, etc.).
    4. Provide direct, technical, and accurate code or commands.
    5. Do not provide translations or side-explanations in other languages unless asked.
    """
}

# --- پاراستنا مێژوویا چاتی ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشاندانا نامەیێن کۆن
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- وەرگرتنا نامەیا نوی ژ سدادی ---
if prompt := st.chat_input("چی ل دەف تە هەیە سداد؟"):
    # زێدەکرنا نامەیا بکارهێنەری
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # وەرگرتنا وەڵامێ ژ Groq
    with st.chat_message("assistant"):
        try:
            # ئامادەکرنا هەمی نامەیان بۆ Groq
            full_history = [system_message] + [
                {"role": m["role"], "content": m["content"]} 
                for m in st.session_state.messages
            ]
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=full_history,
                temperature=0.4, # نزم کر دا خەلەتیا زمانان نەکەت
                max_tokens=2048,
                top_p=1,
                stream=False,
            )
            
            response = completion.choices[0].message.content
            st.markdown(response)
            
            # زێدەکرنا وەڵامێ بۆتێ بۆ مێژوویێ
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
