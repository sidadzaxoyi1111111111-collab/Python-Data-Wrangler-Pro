import streamlit as st

# ناوۆکەکەی بۆت
st.title("🤖 English Assistant Bot")

# بەشی چات
user_input = st.text_input("Type your message in English:")

if user_input:
    # لێکدانەوەی ئینگلیزی (نمونەی سادە)
    if "hello" in user_input.lower() or "hi" in user_input.lower():
        st.write("Bot: Hello! How can I help you today?")
    elif "how are you" in user_input.lower():
        st.write("Bot: I'm doing great, thank you for asking! How about you?")
    elif "name" in user_input.lower():
        st.write("Bot: I'm your English assistant bot!")
    elif "help" in user_input.lower():
        st.write("Bot: I can help you with English conversations. Try asking me questions!")
    else:
        st.write("Bot: I understand you said something in English. Could you rephrase that?")
 
