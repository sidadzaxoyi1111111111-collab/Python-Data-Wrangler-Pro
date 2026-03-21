import telebot
from google import genai
import os

# وەرگرتنا کلیلان ب شێوەیەکێ نهێنی ژ Secrets (ناهێلیت کلیل ئاشکرا ببن)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_KEY')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_KEY)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "سڵاو! ئەز بوتێ سداد ئای مە. ئەز ب زمانی کوردی بادینی بەرسڤا تە ددەم.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"بە زمانی کوردی بادینی وەڵام بدەوە: {message.text}"
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")

bot.infinity_polling()
