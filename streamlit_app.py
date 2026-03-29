# --- پشکا چاتا زیرەک (Beast AI Chat) ---
st.subheader("💬 Ask the Beast")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# گوهۆڕینا نڤیسینێ بۆ شێوازەکێ سادەتر دا تووشی Error نەبی
user_input = st.chat_input("What is the trend for BTC today?")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            chat_completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are 'The Wall Street Beast', a world-class crypto trader helping Sidad Ahmad Mohammed. Be smart and aggressive in English."},
                    *st.session_state.messages
                ]
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"AI Error: {e}")

st.markdown("---")
st.write("© 2026 Sidad AI Project | Powered by Binance & Groq")
