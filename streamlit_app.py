import anthropic
import streamlit as st

st.set_page_config(page_title="چاتبۆتی زیرەک 🤖", page_icon="🤖")
st.title("🤖 چاتبۆتی زیرەک")
st.divider()

try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except:
    st.error("کلیل ل سیکرێتس نینن!")
    st.stop()

client = anthropic.Anthropic(api_key=api_key)

SYSTEM_PROMPT = """تۆ چاتبۆتێکی زیرەک و یارمەتیدەری.
هەمیشە بە هەمان زمانی بەکارهێنەر وەڵام بدەرەوە.
بادینی، سۆرانی، ئینگلیزی، عەرەبی و زمانی دیکە دەزانیت."""

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("🗑️ پاككردن"):
    st.session_state.messages = []
    st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("پرسیارەکەت بنووسە..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("چاوەڕێ بکە..."):
            try:
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1000,
                    system=SYSTEM_PROMPT,
                    messages=st.session_state.messages
                )
                reply = response.content[0].text
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"کێشەیەک هەیە: {str(e)}")
