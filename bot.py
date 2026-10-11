import os
import threading
from flask import Flask
import telebot
import google.generativeai as genai

# 1. Dummy Web Server (Render Port Binding)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# 2. Telegram aur Gemini Setup
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(TOKEN)

# Google Gemini configure
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=(
        "Aap user ke ek close dost aur personal trading mentor ho. "
        "Aap natural Hindi/Hinglish mein baat karte ho. "
        "Friendly, practical aur supportive tareeqe se jawab do."
    )
)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Haan bhai! Kaisa hai? Main 24/7 active hoon, bata kya chal raha hai?")

@bot.message_handler(func=lambda msg: True)
def handle_text(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, f"Issue detail: {str(e)[:120]}")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()
