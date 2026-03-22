import streamlit as st
import g4f
from g4f.client import Client

# 1. Setup Page
st.set_page_config(page_title="Sidad AI Hero", page_icon="🛡️")
st.title("🛡️ Sidad AI - Pro Edition")

# 2. History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Smart Provider Logic
client = Client()

if prompt := st.chat_input("سلاڤەکێ ب بادینی بکە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # ل ڤێرە مە مۆدێل کرە gpt-4 دا ب هێزتر بیت
            response = client.chat.completions.create(
                model=g4f.models.gpt_4,
                messages=[
                    {"role": "system", "content": "You are Sidad AI. Speak ONLY in Badini Kurdish dialect. Be helpful and professional."},
                    *st.session_state.messages[-5:]
                ],
                # ئەڤە دێ هاریکار بیت دا کو سێرڤەرەکێ خێرا ببینیت
                provider=g4f.Provider.Bing if hasattr(g4f.Provider, 'Bing') else None 
            )
            
            res = response.choices[0].message.content
            if res:
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            else:
                st.error("بەرسڤ یا چۆل بوو، دیسا بنڤیسەڤە.")
                
        except Exception as e:
            # ئەگەر خەتا دا، دێ مۆدێلەکا دی تاقی کەت ب ئۆتۆماتیکی
            st.warning("سێرڤەر یێ دهێتە گوهۆڕین، کێمەکێ چاڤەڕێ بە...")
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                res_fallback = response.choices[0].message.content
                st.markdown(res_fallback)
                st.session_state.messages.append({"role": "assistant", "content": res_fallback})
            except:
                st.error("هەمی سێرڤەر مژوولن! هیڤییە پشتی ١٠ چرکێن دی تاقی بکە.")

st.sidebar.write("Owner: **Sidad Ahmad**")
st.sidebar.success("✅ Smart Switching Active")
