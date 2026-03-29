import streamlit as st
from groq import Groq
import yfinance as yf

# ١. گرێدانا کلیلێ ب پاراستی ژ Secrets
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

st.title("🤖 Sidad AI - Bitcoin Advisor")

# ٢. فۆنکشنا وەرگرتنا بهایێ بیتکۆینێ
def get_btc_price():
    btc = yf.Ticker("BTC-USD")
    data = btc.history(period="1d")
    current_price = data['Close'].iloc[-1]
    return round(current_price, 2)

# ٣. شاشا کارکرنێ
if st.button("📊 پشکنینا بازارێ بیتکۆینێ"):
    with st.spinner("Sidad AI یا یێ داتایان ژ بازارێ جیهانی دکێشیت..."):
        price = get_btc_price()
        st.metric(label="بهایێ بیتکۆینێ (USD)", value=f"${price}")
        
        # ناردنا بهای بۆ Groq دا بڕیارێ بدەت
        prompt = f"بهایێ بیتکۆین نوکە {price} دۆلارە. وەک شارەزایەکێ بینانسێ ب زمانێ بادینی بێژە سدادی کا نوکە دەمێ کڕینێ یە یان فرۆتنێ؟ و چەوان خوسارەت نەبیت؟"
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-specdec",
            messages=[{"role": "user", "content": prompt}]
        )
        
        st.subheader("💡 ئامۆژگاریا بوتێ تە:")
        st.write(completion.choices[0].message.content)

st.info("سداد برا، ئەڤە بتنێ ئامۆژگارییە، هەمی پارێ خۆ نەکەیە د مەترسییێ دا!")
