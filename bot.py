import os
import telebot
from google import genai

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(TOKEN)
client = genai.Client(api_key=API_KEY)

user_chats = {}

SYSTEM_INSTRUCTION = (
    "Aap user ke ek close dost aur personal advisor ho. "
    "Aap natural Hinglish mein baat karte ho. "
    "Aap user ko daily planning, trading discipline aur routine mein guide karte ho. "
    "Baat karne ka tareeqa bilkul practical aur supportive hona chahiye."
)

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    user_chats[chat_id] = client.chats.create(
        model="gemini-1.5-flash",
        config=dict(system_instruction=SYSTEM_INSTRUCTION)
    )
    bot.reply_to(message, "Haan bhai! Kaisa hai? Main 24/7 active hoon, bata kya chal raha hai?")

@bot.message_handler(func=lambda msg: True)
def handle_text(message):
    chat_id = message.chat.id
    
    if chat_id not in user_chats:
        user_chats[chat_id] = client.chats.create(
            model="gemini-1.5-flash",
            config=dict(system_instruction=SYSTEM_INSTRUCTION)
        )
        
    try:
        response = user_chats[chat_id].send_message(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Bhai connection issue hua, ek baar dubara message bhejna!")

if __name__ == "__main__":
    bot.infinity_polling()
