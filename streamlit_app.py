import streamlit as st
from groq import Groq

# 1. Secure API Connection
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Page Configuration for a Professional Look
st.set_page_config(page_title="Sidad AI - Beast Mode", page_icon="📈")

st.title("🤖 Sidad AI - Wall Street Beast")
st.markdown("---")

# 2. Define the Brain (Llama 3.3 70B Versatile)
MODEL = "llama-3.3-70b-versatile"

def analyze_trade(buy_price, current_price, quantity):
    # Standard Binance Fee is usually 0.1%
    fee_rate = 0.001 
    
    investment = buy_price * quantity
    current_value = current_price * quantity
    
    # Calculate Fees for both Buying and Selling
    total_fees = (investment * fee_rate) + (current_value * fee_rate)
    
    net_profit = current_value - investment - total_fees
    profit_percentage = (net_profit / investment) * 100

    # Professional Prompt for the AI
    prompt = f"""
    Analysis Request for Sidad Ahmad:
    - Buy Price: {buy_price}
    - Current Price: {current_price}
    - Quantity: {quantity}
    - Net Profit (after 0.1% fees): {net_profit:.2f}
    - Profit Percentage: {profit_percentage:.2f}%
    
    Strict Rule: Answer ONLY in English. Be a professional aggressive trader. 
    Decide: SELL, HOLD, or BUY MORE.
    """

    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a professional Wall Street analyst. Strictly English only. No other languages allowed."},
                {"role": "user", "content": prompt}
            ]
        )
        return net_profit, profit_percentage, completion.choices[0].message.content
    except Exception as e:
        return None, None, f"Error: {e}"

# 3. User Interface (The Calculator)
col1, col2, col3 = st.columns(3)
with col1:
    buy_p = st.number_input("Buy Price (USD)", min_value=0.0)
with col2:
    curr_p = st.number_input("Current Price (USD)", min_value=0.0)
with col3:
    qty = st.number_input("Quantity", min_value=0.0)

if st.button("RUN BEAST ANALYSIS"):
    if buy_p > 0 and curr_p > 0 and qty > 0:
        net, percent, advice = analyze_trade(buy_p, curr_p, qty)
        
        # Color Logic: Green for Profit, Red for Loss
        if net > 0:
            st.success(f"PROFIT CONFIRMED: +${net:.2f} ({percent:.2f}%)")
            st.balloons()
        else:
            st.error(f"LOSS DETECTED: ${net:.2f} ({percent:.2f}%)")
        
        st.markdown("### 🧠 AI Strategic Advice:")
        st.info(advice)
    else:
        st.warning("Please enter all trade details, Sidad.")

st.markdown("---")
st.caption("Powered by Groq Llama-3.3 | Built for Sidad Ahmad Mohammed")
