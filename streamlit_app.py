import streamlit as st

# 1. نیشاندانا دەق (Text/Title)
st.title("Sidad AI - Crypto Monitor 🚀")
st.write(f"سداد برا، بخێر بێی! ئەڤە داتایێن پشکا Spot نە.")

# 2. نیشاندانا وێنەی (Image)
# ئەگەر وێنە ل ناو فۆڵدەرێ سایتێ تە بیت
st.image("chart.png", caption="ئاستێ نرخێ SOL/USDT", use_column_width=True)

# یان ئەگەر وێنە ژ لینەکێ (URL) بیت
image_url = "https://bin.xyz/live-chart.jpg"
st.image(image_url, caption="چارتێ ڕاستەوڕاست")

# 3. نیشاندانا دەقێ ڕەنگاوڕەنگ (Success/Info)
st.success("قازانج: +$10 (ب سوود وەرگرتن ژ ڤۆچەرا $20)")
