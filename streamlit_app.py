import ccxt # پێدڤییە ل requirements.txt زێدە بکەی: ccxt

# 1. گرێدان دگەل باینانس
exchange = ccxt.binance({
    'apiKey': st.secrets["BINANCE_KEY"],
    'secret': st.secrets["BINANCE_SECRET"],
    'enableRateLimit': True,
})

# 2. فۆنکشنا کڕینێ (Buy SOL)
def execute_buy_order(symbol, amount_usd):
    try:
        # کڕین ب بهایێ بازاڕی (Market Order)
        order = exchange.create_market_buy_order(symbol, amount_usd)
        msg = f"✅ SUCCESS: The Beast bought {symbol} for ${amount_usd}!"
        st.success(msg)
        send_telegram_alert(msg) # ئاگەهدارکرنا تە ل سەر تێلێگرامی
    except Exception as e:
        st.error(f"❌ Trading Error: {e}")

# 3. گوهۆڕینا مێشکێ بوتێ (The Execution Brain)
def check_beast_signals(price):
    resistance_level = 53.20
    if price >= resistance_level:
        if "trade_done" not in st.session_state:
            # ل ڤێرە بوت دێ ب خۆ کڕینێ کەت!
            execute_buy_order('SOL/USDT', 20) # بۆ نموونە ب 20 دولاران دکڕیت
            st.session_state.trade_done = True
