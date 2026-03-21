import streamlit as st
from groq import Groq

# 1. Setup Page
st.set_page_config(page_title="Sidad AI Pro", page_icon="🤖")
st.title("🤖 Sidad AI - Professional Edition")

# 2. API Key
api_key = st.secrets.get("GEMINI_KEY")

if not api_key:
    st.error("⚠️ API Key missing in Secrets!")
else:
    client = Groq(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []
        # نامەیا دەستپێکێ (Greeting)
        welcome_msg = "سلاڤ! خێرهاتی بۆ **Sidad AI**. ئەز ل خزمەتا تەمە ب زمانی بادینی و ئینگلیزیەکا پڕۆفیشنال. How can I assist you today?"
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. ڕێنماییا 'مێشکێ پڕۆفیشنال' (Professional Brain Instructions)
    pro_instructions = (
        "You are Sidad AI, a highly professional AI assistant. "
        "1. LANGUAGES: You are fluent in Professional English and the Badini Kurdish dialect (Zakho/Duhok). "
        "2. BADINI RULES: Never use Sorani. Use only Badini terms. "
        "3. ENGLISH RULES: When asked in English, use high-level, professional, and academic vocabulary. "
        "4. BEHAVIOR: Be concise, smart, and direct. Do not repeat greetings if the conversation is ongoing. "
        "5. KNOWLEDGE: You are an expert in coding, general info, and professional communication."
    )

    if prompt := st.chat_input("Ask something / پسیارەکێ بکە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # ناردنا هەمی دیرۆکا چاتی دا بزانیت چ هاتییە گۆتن
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": pro_instructions},
                        *st.session_state.messages[-10:] # زانیارییا ١٠ نامەیێن دوماهیکێ د مێشکی دا دگریت
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.5, # کێمکرنا خەلەتییان
                )
                
                response_text = chat_completion.choices[0].message.content
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Error: {e}")

st.sidebar.markdown("---")
st.sidebar.write("Owner: **Sidad Ahmad**")
st.sidebar.write("Status: **Professional Mode**")
