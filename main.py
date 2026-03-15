import telebot
import requests
import json

# کلیلێن تە (Tokens)
BOT_TOKEN = "8753625924:AAGWIKUWG_hZYEVgKL_Z_vwFGnrCReZFXEQ"
GEMINI_KEY = "AIzaSyBwdP1pEXsVECENx9VJRlW-8BTJEA7Cgek"

bot = telebot.TeleBot(BOT_TOKEN)

def get_ai_response(user_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts": [{"text": f"تۆ Sidad AI یی، ب کوردیەکا بادینی یا کورت بەرسڤ بدە: {user_text}"}]}]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    except:
        return "ببوورە برا، مێشکێ من تۆزەکێ مژیول بوو. جارەکا دی هەوڵ بدە."

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    answer = get_ai_response(message.text)
    bot.reply_to(message, answer)

print("🚀 Sidad Bot is Running...")
bot.infinity_polling()
