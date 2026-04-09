import streamlit as st
from groq import Groq
import base64

# --- ڕێکخستنا لاپەڕەی ---
st.set_page_config(page_title="Sidad AI Master", page_icon="🤖")

# --- وەرگرتنا کلیلێ ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🤖 Sidad AI Master")

# --- پشکا وێنەیان (Sidebar) ---
with st.sidebar:
    st.header("📸 پشکا وێنەیان")
    uploaded_file = st.file_uploader("وێنەیەکێ هەلبژێرە", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="وێنەیێ تە", use_container_width=True)

# --- مێژوویا چاتی ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- وەرگرتنا نامەیێ ---
if prompt := st.chat_input("چی ل دەف تە هەیە؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # ئەگەر وێنە بارکری بیت
            if uploaded_file:
                # خواندنا وێنەی ب شێوەیەکێ دروست
                bytes_data = uploaded_file.getvalue()
                base64_image = base64.b64encode(bytes_data).decode('utf-8')
                
                response = client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                                }
                            ]
                        }
                    ]
                )
                full_response = response.choices[0].message.content
            else:
                # ئەگەر تەنێ نڤیسین بیت
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                full_response = response.choices[0].message.content
            
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"❌ کێشەیەکا تەکنیکی هەبوو: {str(e)}")
