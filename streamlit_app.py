import streamlit as st
import requests
from groq import Groq

# 1. فۆنکشنا پشکنینا خودکار (ئەوا تە داخواز کری)
def check_beast_signals(current_price, rsi, macd_signal):
    resistance = 53.20
    if current_price >= resistance and rsi > 50 and macd_signal == "Bullish":
        st.balloons() # ئاهەنگێ بگێڕە!
        st.success(f"🚀 SIDAD! THE BEAST SAYS GO LONG NOW! (Price: ${current_price})")
        return True
    else:
        st.info(f"⏳ Beast Status: Staying patient at ${current_price}. Waiting for ${resistance}.")
        return False

# --- دەسپێکا لاپەرەی ---
st.title("🦾 Sidad AI - Wall Street Beast")

# 2. کلیلێن Groq
groq_client = Groq(api_key=st.secrets["GROQ_KEY"])

# 3. پشکا داتایێن "Live" (ب ڕێکا Requests بۆ بڕینا بلۆکا باینانس)
def get_live_data():
    # ئەڤە نموونەیە بۆ دراڤەکێ وەک SOL یان AVAX کو نێزیکی $50 بن
    url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
    try:
        data = requests.get(url).json()
        price = data['solana']['usd']
        return price
    except:
        return 52.80 # نرخەکێ وەهمی ئەگەر ئینتەرنێت نەمینیت

current_price = get_live_data()

# 4. ل ڤێرێ فۆنکشنا تە بانگ دکەین
# (تێبینی: ل داهاتی دێ RSI و MACD ژی ب ئۆتۆماتیکی دەرێخین)
check_beast_signals(current_price, rsi=55, macd_signal="Bullish")

st.markdown("---")

# 5. پشکا چاتا زیرەک (Groq)
user_input = st.chat_input("Ask The Beast for the next move...")
if user_input:
    # لێرە کۆدێ چاتێ یێ جاران دانی...
    st.write(f"The Beast is analyzing: {user_input}")
