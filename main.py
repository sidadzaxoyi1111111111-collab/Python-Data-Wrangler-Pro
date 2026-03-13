import telebot
import os

# وەرگرتنا کلیلێ ژ Variables یێن Railway
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# کاتێ ئێک بێژیت "سڵاو" یان "سلاف"
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if "سلاف" in message.text or "سڵاو" in message.text:
        bot.reply_to(message, "سڵاو سیداد برا! بۆتێ تە نوکە یێ کار دکەت و یێ بیدارە. 🚀")
    else:
        bot.reply_to(message, "فەرموو برا، ئەز یێ ل ڤێرە مە دا خزمەتا تە بکەم.")

# دەستپێکرنا بۆتی
print("بۆت نوکە یێ کار دکەت...")
bot.polling()
