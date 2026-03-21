import streamlit as st
from groq import Groq

# 1. Setup Page
st.set_page_config(page_title="Sidad AI - Badini", page_icon="🤖")
st.title("🤖 Sidad AI (Badini Mode)")

# 2. API Key
api_key = st.secrets.get("GEMINI_KEY")

if not api_key:
    st.error("⚠️ کلیل ل ناڤ Secrets نەهاتییە دیتن!")
else:
    client = Groq(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. ڕێنماییا زۆر توند بۆ بادینی (Strict Badini Policy)
    badini_instructions = (
        "Role: You are Sidad AI, a native speaker of the Badini dialect from Zakho/Duhok. "
        "CRITICAL RULE: NEVER use Sorani Kurdish words like (چۆنیت، دەکەم، دەچم، ئەکەم، دەڕۆم، بووم، سپاس، تکایە). "
        "INSTEAD, ALWAYS use Badini words: (چەوانی، دکەم، دچم، من دڤێت، سوپاس، کەرەم بکە، چێدبیت، نینە). "
        "Your language must be 100% Badini. If the user says 'سڵاو', you must reply with 'سلاڤ، چەوانی، باشی؟'. "
        "Do not use 'هیوادارم'، use 'هیڤیدارم'. Do not use 'بەیانیت باش'، use 'سپێدە باش'."
    )

    if prompt := st.chat_input("پسیارەکێ ب بادینی بکە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": badini_instructions},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.4, # نزمکرنا پلەیێ دا پتر پابەندی ڕێنماییا بیت
                )
                
                response_text = chat_completion.choices[0].message.content
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Error: {e}")

st.sidebar.write("Developed by: **Sidad Ahmad**")
