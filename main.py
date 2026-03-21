import telebot
from google import genai
import os

# وەرگرتنا کلیلان ب شێوەیەکێ پاراستی ژ سیستەمی
# ئەڤە ناهێلیت کلیلێن تە ل سەر GitHub ئاشکرا ببن
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_KEY')

# دەسپێکرنا بوتێ تێلێگرامێ
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# دەسپێکرنا مۆدێلا Gemini
client = genai.Client(api_key=GEMINI_KEY)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "سڵاو! ئەز بوتێ سداد ئای (Sidad AI) مە. ئەز دشێم ب زمانی کوردی بادینی بەرسڤا تە بدەم. فەرموو چ پسیارەکا تە هەیە؟")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        # هنارتنا نامێ بۆ Gemini 2.0 Flash
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"تۆ یاریدەدەرێکی زیرەکی، بە زمانی کوردی بادینی وەڵامی ئەمە بدەوە: {message.text}"
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "ببورە، کێشەیەک د پەیوەندیێ دا هەبوو. ل هیڤیێ بە...")
        print(f"Error: {e}")

# دەسپێکرنا کارێ بوتێ
print("Sidad AI is running...")
bot.infinity_polling()
