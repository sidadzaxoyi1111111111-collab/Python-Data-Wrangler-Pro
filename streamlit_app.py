import streamlit as st
import google.generativeai as genai
from PIL import Image

# ١. ڕێکخستنا لاپەرەی بۆ سداد
st.set_page_config(page_title="Sidad AI Agent", page_icon="🤖")

# ٢. خویندنا کلیلێ ب شێوەیەکێ پاراستی ژ Secrets
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
    else:
        st.error("سداد برا، کلیل د ناڤ Secrets دا نینە! ناڤێ وێ بکە: GEMINI_API_KEY")
        st.stop()
except Exception as e:
    st.error(f"کێشەیەک د Secrets دا هەیە: {e}")
    st.stop()

# ٣. دیزاینێ سەرەکی
st.title("🤖 Sidad AI Agent")
st.write("سڵاو سداد برا، ئەز ل خزمەتا تە دام ب زمانێ بادینی.")

# ٤. Sidebar بۆ وێنەیان
with st.sidebar:
    st.header("📸 وێنە دابەزینە")
    uploaded_file = st.file_uploader("وێنەیەکێ هەڵبژێرە...", type=["jpg", "png", "jpeg"])
    st.info("سداد، تو ٢٥ سالی و ل زاخۆ یی. ئەڤ بوتە یێ پاراستییە.")

# ٥. ناساندنا مۆدێلی ب شێوەیەکێ مسۆگەر
# مە ناڤێ مۆدێلی کرە 'gemini-1.5-flash' چونکی باوەرپێکریترینە
model = genai.GenerativeModel('gemini-1.5-flash')

# ٦. مێژوویا چاتی (دا چات بەرزە نەبیت)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ٧. وەرگرتنا رسالێ و بەرسڤدان
user_input = st.chat_input("تشتەکی ب بێژە برا...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Sidad AI یا یێ فکریە..."):
            try:
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([user_input, img])
                else:
                    # مەجبورکرنا بوتێ دا ب بادینی بەرسڤ بدەت
                    full_prompt = f"بەرسڤێ ب زمانێ بادینی بدە: {user_input}"
                    response = model.generate_content(full_prompt)
                
                bot_response = response.text
                st.markdown(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
            except Exception as e:
                st.error(f"خەلەتییەک چێ بوو: {e}")
