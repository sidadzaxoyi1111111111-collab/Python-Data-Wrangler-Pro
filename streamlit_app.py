import streamlit as st
from groq import Groq

# 1. Setup Page
st.set_page_config(page_title="Sidad AI Pro", page_icon="🤖")
st.title("🤖 Sidad AI - Professional Edition")

# 2. API Key from Secrets
api_key = st.secrets.get("GEMINI_KEY")

if not api_key:
    st.error("⚠️ API Key is missing!")
else:
    client = Groq(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []
        welcome_msg = "خێرهاتی بۆ **Sidad AI**. ئەز یێ ل ڤێرێ مە دا ب شێوەیەکێ پڕۆفیشنال هاریکارییا تە بکەم. How can I help you today?"
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. ڕێنماییا 'فول مێشک' (Advanced Instruction)
    pro_logic = (
        "You are Sidad AI, a high-level professional assistant. "
        "STRICT LANGUAGE RULES:\n"
        "- Dialect: Pure Badini (Kurmanji). NEVER use Sorani verb patterns like 'چۆن دکەم' or 'یارمەتیتان بکەم'.\n"
        "- Correct Patterns: Instead of 'یارمەتی دەکەم', use 'هاریکارییا تە دکەم'. Instead of 'چۆنیت', use 'چەوانی'.\n"
        "- Forbidden words: (چۆن، یارمەتی، دەکەم، ئەکەم، دەچم، بەیانیت باش).\n"
        "- Approved words: (چەوا، هاریکاری، دکەم، دچم، سپێدە باش، سوپاس، دڤێت).\n"
        "- English: Use C1/C2 level professional English for technical queries.\n"
        "- Tone: Helpful, direct, and very smart."
    )

    if prompt := st.chat_input("Ask something / پسیارەکێ بکە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": pro_logic},
                        *st.session_state.messages[-6:] # مێشکێ وی یێ ٦ نامەیێن دوماهیکێ
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.3, # کێمکرنا "خەونێن" مۆدێلێ و زێدەکرنا ڕاستیێ
                )
                
                response_text = chat_completion.choices[0].message.content
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Error: {e}")

st.sidebar.markdown("---")
st.sidebar.write("Owner: **Sidad Ahmad**")
st.sidebar.write("System: **Llama 3.3 Pro**")
