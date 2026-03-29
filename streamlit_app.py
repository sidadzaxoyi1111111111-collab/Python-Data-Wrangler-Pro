if prompt := st.chat_input("What is the trend for BTC today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # ل ڤێرێ بانگا Groq دکەین بۆ بەرسڤدانێ
            chat_completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are 'The Wall Street Beast', a world-class crypto trader. You are helping Sidad Ahmad Mohammed. Be smart, aggressive, and provide real insights in English."},
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
