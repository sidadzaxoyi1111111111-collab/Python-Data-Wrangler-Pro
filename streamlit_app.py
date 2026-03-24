import streamlit as st
from groq import Groq

# 1. ڕێکخستنا لاپەرەی و ڕەنگان
st.set_page_config(page_title="Sidad AI Agent", page_icon="👤", layout="centered")

# ستایلێ CSS بۆ جوانکرنا شێوازێ مەسجان (وەک تێلێگرام و واتس ئەپ)
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .main {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Sidad AI Agent")
st.info("سڵاو سداد برا، ئەز ل خزمەتا تە دام ب زمانێ بادینی.")

# 2. وەرگرتنا کلیلێ ژ Secrets
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    # دروستکرنا "بیردۆکا چاتێ" (Chat History) دا مێشکێ وی ڤالا نەبیت
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # نیشادانا مەسجێن کەفن د ناڤ چاتێ دا
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. جهێ نڤێسینا مەسجا نوی (Chat Input)
    if prompt := st.chat_input("تشتەکێ ب بێژە برا..."):
        # زێدەکرنا مەسجا تە بۆ لیستێ
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # بەرسڤا AI
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # ناردنا مەسجێ بۆ مۆدێلێ Llama 3.1
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "تو یاریدەدەرەکێ زیرەکی ناڤێ تە (Sidad AI Agent)ـە. "
                                "تو یێ هاتییە چێکرن بۆ سداد ئەحمەد محەمەد، کو گەشەپێدەرەکێ پایتۆن یێ زیرەکە و خەلکێ زاخۆیە. "
                                "پێدڤییە تەنێ ب زمانێ کوردی شێوەزارێ بادینی (زاخۆیی) باخڤی. "
                                "شێوازێ ئاخفتنا تە بلا برایانە و ڕاقی بیت، نە وەک ڕۆبۆتەکێ بیت. "
                                "هەردەم بێژە 'سداد برا' یان 'برا گیان'."
                            )
                        },
                        *[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                    ],
                    model="llama-3.1-8b-instant",
                    stream=False,
                )
                
                full_response = chat_completion.choices[0].message.content
                message_placeholder.markdown(full_response)
                
                # پاشکەفتکرنا بەرسڤێ دا ژ بیر نەکەت
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"ئاریشەیەک چێبوو: {e}")

else:
    st.error("کلیل د Secrets دا نینە!")
