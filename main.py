import telebot
import os

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def reply_to_all(message):
    user_text = message.text
    
    if "سلاف" in user_text or "سڵاو" in user_text:
        bot.reply_to(message, "سلاف سیداد برا! گەلاوێژا من گەرمە بۆ تە، فەرموو پرسیار بکە.")
    
    elif "چەوای" in user_text or "باشی" in user_text:
        bot.reply_to(message, "ئەز گەلەک باشم سوپاس بۆ خودێ، تو چەوای؟")
        
    elif "دێ تە فرکم" in user_text:
        bot.reply_to(message, "هاهاها! نە برا، من نەفرکێنە، ئەز یێ ل ڤێرە مە دا خزمەتا تە بکەم. 😂")

    else:
        # ل شوینا وێ جۆملا کۆن، بلا نوکە بێژیت:
        bot.reply_to(message, f"وەڵاهی سیداد برا، ل سەر ڤێ پەیڤا '{user_text}' ئەز دێ کێمەکێ لێ کۆڵینەوە کەم!")

bot.polling()
import telebot
import os

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def reply_to_all(message):
    user_text = message.text
    
    # ١. ئەگەر پرسیار ل دۆر پایتۆن کر
    if "پایتون" in user_text or "python" in user_text.lower():
        bot.reply_to(message, "بەلێ سیداد برا! ئەز ب پایتۆن هاتیمە دروستکرن، پایتۆن زمانەکێ گەلەک خوش و ب هێزە. تو دڤێت فێری چی ببی؟")
    
    # ٢. ئەگەر سلاڤ کر
    elif "سلاف" in user_text or "سڵاو" in user_text:
        bot.reply_to(message, "سلاف سیداد برا! گەلاوێژا من گەرمە بۆ تە، فەرموو.")

    # ٣. ئەگەر پرسیارا حالێ وی کر
    elif "چەوای" in user_text or "باشی" in user_text:
        bot.reply_to(message, "ئەز گەلەک باشم سوپاس بۆ خودێ، تو چەوای؟")

    # ٤. هەر تشتەکێ دی
    else:
        bot.reply_to(message, f"سیداد برا، ڤێ پەیڤا '{user_text}' بۆ من یا نوویە، بەس ئەز دێ هەوڵ دەم تێبگەهم!")

bot.polling()
