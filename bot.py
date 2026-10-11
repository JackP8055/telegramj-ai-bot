import os
import threading
from flask import Flask
import telebot
from google import genai

# 1. Render Port Binding
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# 2. Telegram & Gemini Setup
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(TOKEN)
client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = (
    "Aap user ke ek close dost, trading mentor aur personal guide ho. "
    "Aap bilkul natural Hindi/Hinglish mein baat karte ho. "
    "User ke sawalon ka seedha, friendly aur helpful jawab do."
)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Haan bhai! Kaisa hai? Main 24/7 live hoon, bata kya haal chaal?")

@bot.message_handler(func=lambda msg: True)
def handle_text(message):
    try:
        # Direct prompt ke sath Gemini 1.5 Flash ko call
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {message.text}\nAI Dost:"
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=full_prompt
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error details: {e}")
        bot.reply_to(message, f"Issue detail: {str(e)[:100]}")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()
