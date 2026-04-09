import streamlit as st
from groq import Groq
import base64

# --- ڕێکخستنا لاپەڕەی ---
st.set_page_config(page_title="Sidad AI Vision", page_icon="👁️")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🤖 Sidad AI Master")

# --- ل ڤێرێ جهێ وێنەی زێدە بوو (Sidebar) ---
with st.sidebar:
    st.header("📸 پشکا وێنەیان")
    uploaded_file = st.file_uploader("وێنەیەکێ ل ڤێرێ بار بکە...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="وێنەیێ بارکری", use_container_width=True)

# --- پاراستنا مێژوویا چاتی ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- وەرگرتنا نامەیا نوی ---
if prompt := st.chat_input("چی ل دەف تە هەیە سداد؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # ئەگەر وێنە هەبیت، مۆدێلا Vision بکار دئینین
            if uploaded_file:
                image_data = base64.b64encode(uploaded_file.read()).decode("utf-8")
                image_url = f"data:image/jpeg;base64,{image_data}"
                
                messages = [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": image_url}}
                        ]
                    }
                ]
                model_name = "llama-3.2-11b-vision-preview"
            else:
                # ئەگەر تەنێ نامە بیت، مۆدێلا ئاسایی بکار دئینین
                messages = [{"role": "system", "content": "You are Sidad AI Master. Respond in Badini Kurdish."}]
                for m in st.session_state.messages:
                    messages.append({"role": m["role"], "content": m["content"]})
                model_name = "llama-3.3-70b-versatile"

            completion = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.4
            )
            
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
