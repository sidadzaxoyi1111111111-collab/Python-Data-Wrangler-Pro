import streamlit as st
from binance.client import Client
from groq import Groq

# هەوڵدان بۆ گرێدانێ ب بێ بەربەست
try:
    # ⚠️ ل ڤێرێ مە 'tld="me"' یان 'tld="us"' زێدە کر دا ئەگەر وڵاتەک قەدەغە بیت، بچیتە سەر ئێکێ دی
    client = Client(
        st.secrets["BINANCE_KEY"], 
        st.secrets["BINANCE_SECRET"],
        tld='me' # ئەڤە هندەک جاران کێشەیا وڵاتی چاک دکەت
    )
    # ئەگەر هێشتا هەر Error هەبوو، پێدڤییە ڤێ تاقی بکەی:
    # client.API_URL = 'https://api.binance.us' 
    
    groq_client = Groq(api_key=st.secrets["GROQ_KEY"])
    st.sidebar.success("✅ Connected (Bypassing Restrictions)")
except Exception as e:
    st.sidebar.error(f"🌍 Location Error: {e}")
    st.stop()
