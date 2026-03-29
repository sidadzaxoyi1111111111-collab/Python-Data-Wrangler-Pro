import streamlit as st
import google.generativeai as genai
from PIL import Image

# ١. ڕێکخستنا لاپەرەی بۆ سداد
st.set_page_config(page_title="Sidad AI Agent", page_icon="🤖", layout="centered")

# ٢. دیزاینێ سەرەکی یێ سایتێ سداد
st.markdown("""
<div style="background-color: #0c1a2c; padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #1f3a5f;">
    <h1 style="color: white; margin-bottom: 0;">🤖 Sidad AI Agent</h1>
    <p style="color: #6c99cb; font-size: 18px; direction: rtl;">سڵاو سداد برا، ئەز ل خزمەتا تە دام ب مێشکێ Gemini 2.0 Flash.</p>
</div>
""", unsafe_allow_html=True)

# ٣. خویندنا کلیلا ڤەشارتی ژ Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("سداد برا، کلیل د ناڤ Secrets دا نەهاتییە دیتن! ناڤێ وێ بکە: GEMINI_API_KEY")
    st.stop()

# ٤. Sidebar بۆ وێنەیان
with st.sidebar:
    st.header("📸 وێنە دابەزینە")
    uploaded_file = st.file_uploader("وێنەیەکێ هەڵبژێرە (JPG, PNG)...", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption='وێنێ تە ئامادەیە', use_column_width=True)
    st.info("سداد، تو ٢٥ سالی و ل زاخۆ یی. ئەڤ بوتە یێ پاراستییە.")

# ٥. دروستکرنا مێشکێ Gemini 2.0 Flash
# ئەڤە ناڤێ دروست یێ مۆدێلی یە دا کێشەیا 404 چارەسەر ببت
system_prompt = "ناڤێ تە Sidad AI Agent یە. تو ب زمانێ بادینی دئاخڤی و ئینگلیزییا تە فولە. تو وێنەیان دناسی."
model = genai.GenerativeModel(model_name='gemini-2.0-flash-exp', system_instruction=system_prompt)

# ٦. پاراستنا مێژوویا چاتی
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ٧. وەرگرتنا رسالێ و بەرسڤدان
user_input = st.chat_input("تشتەکی ب بێژە برا...")

if user_input:
    # نیشادانا پرسیارا سداد
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # بەرسڤدانا AI
    with st.chat_message("assistant"):
        with st.spinner("Sidad AI یا یێ فکریە..."):
            try:
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([user_input, img])
                else:
                    response = model.generate_content(user_input)
                
                bot_response = response.text
                st.markdown(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
            except Exception as e:
                st.error(f"خەلەتییەک چێ بوو: {e}")
