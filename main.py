import telebot
from google import genai

# کلیلێن تە یێن نوو
GEMINI_KEY = 'AIzaSyCHpLbDrdwt8QDB5e-n7aZBvaTh0pwZws4'
TELEGRAM_TOKEN = '8526936532:AAGYPz-oF0Z99Tafw_HB7en82cnZ7oc3650'

client = genai.Client(api_key=GEMINI_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=f"تۆ یاریدەدەرێکی زیرەکی، بە زمانی کوردی بادینی وەڵامی سیداد بدەوە: {message.text}"
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")

print("🚀 سیداد، بۆتێ تە نوکە یێ چالاکە...")
bot.infinity_polling()
