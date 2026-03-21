import streamlit as st
from groq import Groq

# 1. Setup Page
st.set_page_config(page_title="Sidad AI Giant", page_icon="🌐", layout="wide")
st.title("🌐 Sidad AI - Giant Model Edition")
st.markdown("---")

# 2. API Key
api_key = st.secrets.get("GEMINI_KEY")

if not api_key:
    st.error("⚠️ API Key is missing!")
else:
    client = Groq(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []
        welcome = "خێرهاتی بۆ ڤێرژنا عیملاق یا **Sidad AI**. ئەز نوکە ب مێشکەکێ زۆر مەزن دئاخڤم. How can I assist you?"
        st.session_state.messages.append({"role": "assistant", "content": welcome})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. ڕێنماییا مێشکێ عیملاق (Giant Brain Instructions)
    # ئەڤە ڕێنماییەکا زۆر پڕۆفیشنالە بۆ مۆدێلێن مەزن
    giant_logic = (
        "You are Sidad AI, powered by the world's most powerful open-weights model. "
        "Your creator is Sidad Ahmad, a professional Python developer.\n"
        "RULES:\n"
        "- LANGUAGE: Pure Badini Kurdish for local talk. Professional English for technical talk.\n"
        "- KNOWLEDGE: You are an expert in Data Science, Automation, and Python.\n"
        "- BEHAVIOR: Be extremely smart, precise, and helpful. No Sorani words allowed.\n"
        "- BADINI EXAMPLES: (دکەم، دچم، دڤێت، چەوانی، سوپاس، سپێدە باش)."
    )

    if prompt := st.chat_input("پسیارەکا ئالۆز بکە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # بکارئینانا مۆدێلا عیملاق Llama 3.1 405B
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": giant_logic},
                        *st.session_state.messages[-8:]
                    ],
                    model="llama-3.1-405b-reasoning", # ئەڤە مۆدێلا عیملاقە
                    temperature=0.3,
                )
                
                response_text = chat_completion.choices[0].message.content
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                # ئەگەر 405B ل دەف تە قەرەبالغ بوو، ئەڤێ تاقی بکە: llama-3.3-70b-versatile
                st.warning("مۆدێلا عیملاق یا مژوولە، ئەز دێ ب مۆدێلا 70B بەرسڤێ دەم...")
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "system", "content": giant_logic}, *st.session_state.messages[-5:]],
                    model="llama-3.3-70b-versatile",
                    temperature=0.3,
                )
                response_text = chat_completion.choices[0].message.content
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})

st.sidebar.markdown("---")
st.sidebar.write("Owner: **Sidad Ahmad**")
st.sidebar.write("Model: **Llama 405B / 70B**")
