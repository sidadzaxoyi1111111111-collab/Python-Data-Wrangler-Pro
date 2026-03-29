import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# ١. ناڤ و نیشانێ سایتێ سداد (مۆبایلا Infinix Pro Note 50)
st.set_page_config(page_title="Sidad AI Agent", page_icon="🤖", layout="wide")

# ٢. دیزاینێ جوان یێ "سڵاو سداد برا"
st.markdown("""
<div style="background-color: #0c1a2c; padding: 20px; border-radius: 15px; border: 1px solid #1f3a5f;">
    <h1 style="color: white; text-align: center; font-size: 36px; margin-bottom: 5px;">🤖 Sidad AI Agent</h1>
    <p style="color: #6c99cb; text-align: center; font-size: 18px; margin-top: 0;">.سڵاو سداد برا، ئەز ل خزمەتا تە دام ب زمانێ بادینی ۆو ئینگلیزی</p>
</div>
""", unsafe_allow_html=True)

# ٣. چێکرنا جهێ کلیلێ API (ل لایێ چەپێ)
with st.sidebar:
    st.title("🛠️ تنظیمات و ئامرازێن سداد")
    api_key = st.text_input("کلیلێ Google Gemini API ل ڤێرە دانی برا:", type="password")
    
    # ٤. دابەزاندنا وێنەی (File Uploader) بۆ مۆڵتیمۆدال
    uploaded_file = st.file_uploader("وێنەیەکێ هەڵبژێرە (JPG, PNG)...", type=["jpg", "png", "jpeg"])
    
    # نیشادانا وێنەی ئەگەر هاتە هەڵبژاردن
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='وێنێ تە یێ هاتییە دابەزاندن', use_column_width=True)
    
    st.markdown("---")
    st.info("سداد برا، تو ٢٥ سالی و ل سەر پایتۆن و AI کار دکەی. ئەڤ بوتە یێ پاراستییە.")

# ٥. چێکرنا مێشکێ بوتێ Gemini
if api_key:
    genai.configure(api_key=api_key)
    
    # سیستەمێ پڕۆمپتێ سداد (بۆ بادینی و ئینگلیزییا فول)
    system_instruction = """
    ناڤێ تە "Sidad AI Agent" یە و تو یێ تایبەتی بۆ "سداد" (گەنجەکێ ٢٥ سالی ل زاخۆ، عیراق، کو شارەزایە د پایتۆن و داتا سپێشالیست دا).
    تو زۆر ب جوانی و بێ کێشە ب زمانێ بادینی دئاخڤی، لێ تو ب زمانێ ئینگلیزی ژی فول فول و ب شێوەیەکێ ئەکادیمی و زانستی دزانی، و هەر زمانەکێ دی یێ جیهانی.
    ئەگەر سداد ب بادینی پرسیار کر، ب بادینی بەرسڤێ بدە. ئەگەر ب ئینگلیزی پرسیار کر، ب ئینگلیزی فول بەرسڤێ بدە. ئەگەر وێنەیەک بۆ تە فرێکر، زۆر ب دقیقی ڕونکردنەوە بدە، ئەگەر نرخێن دراڤان ژ **Binance** تێدا هەبوون، کێشەی نەبیت تێبگەهه (لێ چ جاران داخوازا کلیلێن والیتێ (Seed Phrase) نەکه چونکی تو بوتێ پاراستی یی).
    هەروەسا تو شارەزای د پایتۆن دا و تو دشێی کێشەیێن کۆدی یێن سداد چارەسەر بکەی، بۆ نموونە کێشەیێن **Terminal** یان **Bash** ل سەر PythonAnywhere.
    """
    model = genai.GenerativeModel('gemini-1.5-pro-latest', system_instruction=system_instruction)
else:
    st.warning("سداد برا، کلیلێ (API Key) ل لایێ چەپێ دانی دا بوت کار بکت.")
    st.stop()

# ٦. مێژوویا چاتی (Chat History)
if "messages" not in st.session_state:
    st.session_state.messages = []

# نیشادانا نامەیێن کۆن
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "image" in message:
            st.image(message["image"], use_column_width=False, width=200)

# ٧. وەرگرتنا رسالا سداد ل خوارێ (Chat Input)
user_input = st.chat_input("تشتەکی ب بێژە یان وێنەیەکێ پرسیار بکە برا...")

# ٨. بەرسڤدانا سداد (وێنە + نڤیسین)
if user_input:
    # زێدەکرنا پرسیارا سداد د مێژوویێ دا
    message_data = {"role": "user", "content": user_input}
    if uploaded_file is not None:
        message_data["image"] = uploaded_file
    st.session_state.messages.append(message_data)
    
    with st.chat_message("user"):
        st.write(user_input)
        if uploaded_file is not None:
            st.image(uploaded_file, use_column_width=False, width=200)

    # بەرسڤدانا بوتێ سداد
    with st.chat_message("assistant"):
        with st.spinner("Sidad AI Agent یا یێ فکریە..."):
            try:
                # ئەگەر وێنە هەبیت
                if uploaded_file is not None:
                    # گوهۆڕینا وێنەی بۆ جۆرێ (Byte array) بۆ Gemini
                    uploaded_file.seek(0)
                    image_data = uploaded_file.read()
                    image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
                    
                    response = model.generate_content([user_input, image_parts[0]])
                # ئەگەر بتنێ نڤیسین بیت
                else:
                    response = model.generate_content(user_input)
                
                # نیشادانا بەرسڤێ و پاشکەوتکرن
                bot_response = response.text
                st.write(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                
            except Exception as e:
                st.error(f"سداد برا، خەلەتییەک چێ بوو: {e}")
