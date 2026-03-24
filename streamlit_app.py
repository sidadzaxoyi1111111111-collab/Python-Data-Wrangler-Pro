import streamlit as st
from groq import Groq

# ڕێکخستنا لاپەرەی ب ناڤێ سدادی
st.set_page_config(page_title="Sidad AI Wrangler", page_icon="🤖")

st.title("🤖 Sidad AI Wrangler")
st.subheader("ب خێر بێی سداد! ئەڤە مێشکێ Groq یێ خێرایە.")

# وەرگرتنا کلیلێ ژ Secrets ب شێوەیەکێ پاراستی
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    st.success("✅ کلیلێن Secrets ب سەرکەفتی هاتنە ناساندن.")

    # جهێ نڤێسینا پرسیارێ
    user_input = st.text_input("پرسیارەکێ ب زاخۆیی بکە (بۆ نموونە: ئەز کێم؟):")

    if user_input:
        with st.spinner('دێ مێشکێ خۆ گەرم کەم...'):
            try:
                # ناردنا پرسیارێ بۆ مۆدێلێ Llama 3
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "تو یاریدەدەرەکێ زیرەکی، ناڤێ تە Sidad AI Wrangler e. بەرسڤێ ب کوردی بادینی شێوەزارێ زاخۆ بدە. سداد دەرچوویێ کۆمپیوتەری یە و پایتۆن گەشەپێدەرە، ب ڕێز باخڤە."
                        },
                        {
                            "role": "user",
                            "content": user_input,
                        }
                    ],
                    model="llama3-8b-8192",
                )
                
                # نیشادانا بەرسڤێ
                st.info(f"🤖 AI دبیژیت: \n\n {chat_completion.choices[0].message.content}")
                
            except Exception as e:
                st.error(f"❌ ئاریشەیەک چێبوو: {e}")
else:
    st.error("❌ سداد، کلیلا GROQ_API_KEY د Secrets دا نینە! وێ دانیە دا کار بکەت.")
