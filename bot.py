import telebot
import requests
import time
from flask import Flask
from threading import Thread

# --- WEB SERVER ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- CONFIG ---
API_TOKEN = '8768167829:AAFuCKoD8_TMkg8Wk_KsNfrsy10RiD-d4dI'
bot = telebot.TeleBot(API_TOKEN, threaded=False)

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🤖 CHAT WITH AI", callback_data="chat_ai"))
    markup.add(telebot.types.InlineKeyboardButton("🔍 TG ID INFO", callback_data="check_tg"))
    bot.send_message(message.chat.id, "💀 **LOSTED BOT IS READY**\n\nChoose an option:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "chat_ai":
        bot.send_message(call.message.chat.id, "🤖 Ask me anything (Reply to this message):", reply_markup=telebot.types.ForceReply())
    elif call.data == "check_tg":
        bot.send_message(call.message.chat.id, "🔍 Send Telegram User ID:", reply_markup=telebot.types.ForceReply())

@bot.message_handler(func=lambda message: True)
def handle_replies(message):
    if message.reply_to_message:
        text = message.reply_to_message.text
        if "Ask me anything" in text:
            # Smart AI Fallback
            query = message.text
            try:
                # Fast & Stable AI API
                res = requests.get(f"https://api.simsimi.net/v2/?text={query}&lc=en").json()
                bot.reply_to(message, f"🤖 **AI:** {res['success']}")
            except:
                bot.reply_to(message, "❌ AI is taking a nap. Try simple words.")

if __name__ == "__main__":
    keep_alive()
    bot.remove_webhook()
    time.sleep(2)
    bot.infinity_polling()
                
