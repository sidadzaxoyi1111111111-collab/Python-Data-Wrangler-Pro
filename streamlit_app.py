import streamlit as st
from groq import Groq

# ١. گرێدانا کلیلێ
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🤖 Sidad AI - Binance Pro")

MODEL = "llama-3.3-70b-versatile"

def sidad_pro_analysis(market_info):
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system", 
                    "content": """
                    You are a High-Frequency Trading Bot for Sidad Ahmad.
                    Language: STRICTLY ENGLISH.
                    Task: Analyze the buying and selling price. 
                    Decision: Instantly say 'PROFIT' or 'LOSS'.
                    Advice: Explain the percentage and if he should sell NOW.
                    """
                },
                {"role": "user", "content": market_info}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# ٣. شاشا کارکرنێ
user_input = st.chat_input("Enter: Buy price, Sell price, and Coin name...")

if user_input:
    with st.spinner("Analyzing Market Data..."):
        response = sidad_pro_analysis(user_input)
        st.success("Analysis Complete!")
        st.markdown(response)
