import telebot
import os
import requests

# کلیلێن پێدڤی
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def get_ai_response(message):
    user_text = message.text
    
    # ئەگەر سلاڤ کر، بلا ب ناڤێ وی بەرسڤ بدەت
    if "سلاف" in user_text or "سڵاو" in user_text:
        bot.reply_to(message, "سلاف سیداد برا، فەرموو هەر پرسیارەکا تە هەبیت ئەز یێ ل ڤێرە مە.")
    else:
        try:
            # ل ڤێرە دێ پەیوەندیێ ب مەکینەکا زیرەک کەین دا بەرسڤێ بدەت
            response = requests.get(f"https://api.simsimi.net/v2/?text={user_text}&lc=ku")
            ai_message = response.json()['success']
            bot.reply_to(message, ai_message)
        except:
            bot.reply_to(message, "ببورە سیداد برا، مێشکێ من نوکە یێ مژوولە، دووبارە پرسیار بکە.")

bot.polling()
