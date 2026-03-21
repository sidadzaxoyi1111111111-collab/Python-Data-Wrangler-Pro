import streamlit as st
from groq import Groq

# 1. Setup Page
st.set_page_config(page_title="Sidad AI - Badini", page_icon="🤖")
st.title("🤖 Sidad AI (Badini Edition)")

# 2. API Key from Secrets
api_key = st.secrets.get("GEMINI_KEY")

if not api_key:
    st.error("⚠️ کلیل ل ناڤ Secrets نەهاتییە دیتن!")
else:
    client = Groq(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # نیشاندانا نامەیێن کۆن
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. ڕێنماییا فول بادینی (System Prompt)
    # ئەڤە ئەو پشکە یا تو دبێژیێ 'فول بادینی'
    badini_instructions = (
        "تۆ Sidad AI، یاریدەدەره‌كێ زیرەکی و ب تنێ ب زارۆکێ بادینی (دەڤەرا بەهدینان - دهۆک، زاخۆ، ئامێدی، ئاکرێ) دئاخڤی. "
        "قەدەغەیە ب سۆرانی باخڤی. پەیڤێن (چۆنیت، دەکەم، دەچم، ناخۆشە) بکار نەئینە. "
        "ل شوونا وان ئەڤان پەیڤان بکار بینە: (چەوانی، دکەم، دچم، نەخۆشە، چێدبیت، هەیە، نینە، من دڤێت). "
        "هەمیشە بێژە 'سلاڤ'، 'کەرەم بکە'، 'ل خزمەتا تەمە'. "
        "ئەگەر پسیار ب ئینگلیزی یان عەرەبی ژی هات، تو هەر ب بادینی بەرسڤێ بدە."
    )

    # 4. Input field
    if prompt := st.chat_input("پسیارەکێ ب بادینی بکە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # ناردنا نامەیێ بۆ Groq ب ڕێنماییا بادینی
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": badini_instructions},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.7, # بۆ هندێ ئاخفتنا وێ سروشتی بیت
                )
                
                response_text = chat_completion.choices[0].message.content
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Error: {e}")

# Sidebar
st.sidebar.markdown("---")
st.sidebar.write("Developed by: **Sidad Ahmad**")
st.sidebar.write("Region: **Behdinan**")
