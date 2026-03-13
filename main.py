import telebot
import os

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def reply_to_all(message):
    user_text = message.text
    
    if "سلاف" in user_text or "سڵاو" in user_text:
        bot.reply_to(message, "سلاف سیداد برا! فەرموو، ئەز یێ ل ڤێرە مە دا هەر پرسیارەکا تە هەبیت بەرسڤ بدەم.")
    elif "ناڤێ تە" in user_text:
        bot.reply_to(message, "ناڤێ من بۆتێ سیدادە، ب شانازی ڤە!")
    elif "باشی" in user_text:
        bot.reply_to(message, "سوپاس بۆ خودێ، ئەگەر تو باش بی ئەز ژی یێ باشم.")
    else:
        # ل شوینا خەتایێ، بلا هەر نامەیەکا تە بۆ تە ڤەگوهێزیتەڤە هەتا کلیلەکا زیرەکتر دابین دکەین
        bot.reply_to(message, f"تە گۆت: {user_text} .. سیداد برا، ئەز هێشتا یێ فێری ڤێ پەیڤێ دبم، بەس تو هەر یا بێژە!")

bot.polling()
