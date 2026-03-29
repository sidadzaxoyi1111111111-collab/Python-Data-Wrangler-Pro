import streamlit as st
from binance.client import Client
from groq import Groq

# هەوڵدان بۆ بڕینا بەربەستێن جوگرافی
try:
    # زێدەکرنا tld='me' یان گوهۆڕینا سێرڤەری بۆ ئەوروپا
    client = Client(
        st.secrets["BINANCE_KEY"], 
        st.secrets["BINANCE_SECRET"],
        tld='me' # ئەڤە یارمەتیدەرە بۆ ئایپیێن بلۆک کری
    )
    
    # ئەگەر هێشتا هەر Error دا، ئەڤێ تاقی بکە:
    # client.API_URL = 'https://api-gcp.binance.com/api' 
    
    groq_client = Groq(api_key=st.secrets["GROQ_KEY"])
    st.sidebar.success("✅ Connected: Location Bypass Active")
except Exception as e:
    st.sidebar.warning(f"⚠️ Binance is restricted here. Switching to AI Mode.")
    # ل ڤێرێ مە مەرجەک دانا دا ئەگەر بینانس کار نەکر، بتنێ چات کار بکەت
    groq_client = Groq(api_key=st.secrets["GROQ_KEY"])
