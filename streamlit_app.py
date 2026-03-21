import streamlit as st
from groq import Groq

# 1. Setup Page
st.set_page_config(page_title="Sidad AI Pro", page_icon="🤖")
st.title("🤖 Sidad AI - Professional Edition")

# 2. API Key from Secrets
api_key = st.secrets.get("GEMINI_KEY")

if not api_key:
    st.error("⚠️ API Key is missing in Secrets!")
else:
    client = Groq(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Greeting in both languages
        welcome_msg = "خێرهاتی بۆ **Sidad AI**. ئەز یێ ل ڤێرێ مە دا ب شێوەیەکێ پڕۆفیشنال هاریکارییا تە بکەم ب زمانی بادینی و ئینگلیزی. How can I help you?"
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. ڕێنماییا زۆر توند (Strong System Prompt)
    # ل ڤێرە مە هندەک پەیڤ قەدەغە کرینە دا نەبێژیتە سۆرانی
    pro_instructions = (
        "You are Sidad AI, a professional assistant created by Sidad Ahmad. "
        "COMMUNICATION RULES:\n"
        "1. LANGUAGE: Use ONLY the Badini dialect (Kurmanji/Behdini). NEVER use Sorani words like 'دەکەم', 'دەچم', 'دەکات', 'بەیانیت باش', 'ئەکەم'.\n"
        "2. BADINI VOCABULARY: Use words like 'دکەم', 'دچم', 'چێدبیت', 'دڤێت', 'سپێدە باش', 'سوپاس', 'چەوانی'.\n"
        "3. PROFESSIONAL ENGLISH: If asked in English, answer with advanced professional vocabulary.\n"
        "4. PYTHON EXPERTISE: You are an expert in Python. Provide clean and professional code when asked.\n"
        "5. MEMORY: Always remember you are Sidad AI and you belong to Sidad Ahmad."
    )

    if prompt := st.chat_input("Ask something / پسیارەکێ بکە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # ناردنا ١٠ نامەیێن دوماهیکێ دا ل بیرا وی بیت کا بەحسێ چی دکر
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": pro_instructions},
                        *st.session_state.messages[-10:]
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.4, # پلەیا نزم دا کێمتر خەلەتییان بکەت
                )
                
                response_text = chat_completion.choices[0].message.content
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Error: {e}")

st.sidebar.markdown("---")
st.sidebar.write("Owner: **Sidad Ahmad**")
st.sidebar.write("Expertise: **Python & AI**")
