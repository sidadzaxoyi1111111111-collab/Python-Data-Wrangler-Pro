import streamlit as st
from groq import Groq

# ڕێکخستنا لاپەرەی
st.set_page_config(page_title="Sidad AI Wrangler", page_icon="🤖")

st.title("🤖 Sidad AI Wrangler")
st.markdown("---")
st.subheader("ب خێر بێی سداد برا! ئەڤە مێشکێ Groq یێ نوی یە.")

# وەرگرتنا کلیلێ ژ Secrets
if "GROQ_API_KEY" in st.secrets:
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        st.success("✅ کلیلێن Secrets کار دکەن.")

        # جهێ نڤێسینا پرسیارێ
        user_input = st.text_input("پرسیارەکێ ب بادینی بکە (بۆ نموونە: چەوایی برا؟):")

        if user_input:
            with st.spinner('دێ مێشکێ خۆ گەرم کەم...'):
                # ل ڤێرێ مە مۆدێل گۆهۆڕی بۆ Llama 3.1 دا خەلەتی نەمینیت
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "تو یاریدەدەرەکێ زیرەکی، ناڤێ تە Sidad AI Wrangler e. "
                                "پێدڤییە تەنێ ب زمانێ کوردی، شێوەزارێ بادینی (زاخۆیی) بەرسڤێ بدەی. "
                                "گەلەک ب ڕێز و برایانە دگەل سدادی باخڤە. "
                                "ئەگەر سدادی ب هەر زمانەکێ دی باخڤیت، تو هەر ب بادینی بەرسڤێ بدە."
                            )
                        },
                        {
                            "role": "user",
                            "content": user_input,
                        }
                    ],
                    model="llama-3.1-8b-instant", # مۆدێلێ نوی یێ کار دکەت
                )
                
                # نیشادانا بەرسڤێ
                answer = chat_completion.choices[0].message.content
                st.info(f"🤖 Sidad AI دبیژیت: \n\n {answer}")
                
    except Exception as e:
        st.error(f"❌ ئاریشەیەک چێبوو: {e}")
else:
    st.error("❌ سداد، کلیلا GROQ_API_KEY د Secrets دا نینە!")
