import streamlit as st
import telebot # پێدڤییە ل requirements.txt بنڤێسی: pyTelegramBotAPI

# 1. کلیلێن تە یێن نوو
TELEGRAM_TOKEN = "8753625924:AAHUBGnKWNUB68h4HwICg3mSwZn9V3j7w1c"
CHAT_ID = "8526936532"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# 2. فۆنکشنا فرێکرنا نامەیان
def send_beast_notification(message):
    try:
        bot.send_message(CHAT_ID, message)
        st.sidebar.success("📡 Telegram Alert Sent!")
    except Exception as e:
        st.sidebar.error(f"Telegram Error: {e}")

# 3. نێچیرڤانێ دەرفەتان (The Opportunity Hunter)
def check_beast_signals(current_price, rsi, macd_signal):
    resistance = 53.20
    # تێبینی: لێرە مە مەرج دانا بۆ هەر بلندبوونەکێ ژ 53.20
    if current_price >= resistance:
        msg = f"🦾 Sidad AI Alert!\n🚀 Price: ${current_price}\n✅ The Beast says: GO LONG NOW!"
        st.success(msg)
        st.balloons()
        send_beast_notification(msg) # لێرە نامە دچیتە تێلێگراما تە
        return True
    return False

# نموونە بۆ تاقیکرنێ
if st.button("Test Telegram Connection"):
    send_beast_notification("✅ Sidad, your AI is now connected to Telegram!")
