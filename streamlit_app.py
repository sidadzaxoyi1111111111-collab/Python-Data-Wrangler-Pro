import streamlit as st
from groq import Groq

# 1. گرێدانا کلیلێ ب پاراستی
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Sidad AI - Hybrid Beast", page_icon="⚡")

st.title("🤖 Sidad AI - Wall Street Beast")
st.markdown("---")

MODEL = "llama-3.3-70b-versatile"

# --- پشکێ ئێکێ: حیسابکەرا بازاری (The Calculator) ---
st.subheader("📊 Trade Calculator")
col1, col2, col3 = st.columns(3)
with col1:
    buy_p = st.number_input("Buy Price (USD)", min_value=0.0, step=0.01)
with col2:
    curr_p = st.number_input("Current Price (USD)", min_value=0.0, step=0.01)
with col3:
    qty = st.number_input("Quantity", min_value=0.0, step=0.0001)

if st.button("RUN BEAST ANALYSIS"):
    if buy_p > 0 and curr_p > 0 and qty > 0:
        investment = buy_p * qty
        current_val = curr_p * qty
        # حیسابکرنا پارێ بینانسێ 0.1%
        net_profit = current_val - investment - (current_val * 0.001) 
        profit_pct = (net_profit / investment) * 100
        
        if net_profit > 0:
            st.success(f"PROFIT: +${net_profit:.2f} ({profit_pct:.2f}%)")
        else:
            st.error(f"LOSS: ${net_profit:.2f} ({profit_pct:.2f}%)")
    else:
        st.warning("Please enter all trade details above, Sidad.")

st.markdown("---")

# --- پشکێ دووێ: چاتا ئینگلیزی (Strictly English Chat) ---
st.subheader("💬 Ask the Beast")

if "messages" not in st.session_state:
    st.session_state.messages = []

# پیشاندانا نامێن کۆن
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# وەرگرتنا پرسیارێن تە ب ئینگلیزی
if prompt := st.chat_input("Ask me anything about the market..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a professional Wall Street trader. Answer ONLY in English. Be aggressive and smart."},
                *st.session_state.messages
            ]
        )
        response = completion.choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

st.caption("Built for Sidad Ahmad Mohammed | Powered by Groq")
