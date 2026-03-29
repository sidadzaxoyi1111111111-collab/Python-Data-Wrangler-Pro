import streamlit as st
import google.generativeai as genai

# لیستا کلیلێن تە (تو دشێی ١٠ دانان ل ڤێرە زێدە بکەی)
api_keys = ["KEY_1", "KEY_2", "KEY_3"] 

st.title("🤖 Sidad AI - The Unstoppable")

def try_keys():
    for key in api_keys:
        try:
            genai.configure(api_key=key)
            # تاقیکرن ب مۆدێلێ جێگیر
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content("سڵاو سداد")
            return response.text
        except Exception as e:
            continue
    return "سداد برا، هەمی کلیل بلۆک بوون!"

if st.button("تاقیکرنا فیلبازیێ"):
    result = try_keys()
    st.write(result)
