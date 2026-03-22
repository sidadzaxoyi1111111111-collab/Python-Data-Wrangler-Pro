# 3. Smart Provider Logic (Updated for Badini)
client = Client()

if prompt := st.chat_input("سلاڤەکێ ب بادینی بکە..."):
    # ل ڤێرە ئەم ڕێنماییا بادینی دگەل هەر پسیارەکێ دفرێکەین دا خەتا نەت
    instruction = "STRICT: Speak ONLY in Badini Kurdish dialect. You are Sidad AI. Answer this: "
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="gpt-4o", 
                messages=[
                    {"role": "system", "content": "You are Sidad AI. Your creator is Sidad Ahmad. Speak only in Badini Kurdish."},
                    {"role": "user", "content": instruction + prompt}
                ]
            )
            res = response.choices[0].message.content
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        except:
            st.error("سێرڤەر مژوولە، دیسا تاقی بکە.")
