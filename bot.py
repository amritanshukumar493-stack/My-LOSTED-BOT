import telebot
import requests
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply

# --- WEB SERVER (For Render 24/7) ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is Running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOT CONFIGURATION ---
# @BotFather se mila TOKEN yahan dalein
API_TOKEN = '8768167829:AAFlWONi10gcAG-m-V7yrDXOcLLQ1zPWo_s' 
bot = telebot.TeleBot(API_TOKEN)

# Stylish Header (Plain text format taaki error na aaye)
HEADER = "╔════════════════╗\n     LOSTED EVERYTHING ❜ ⚚🏴‍☠️\n╚════════════════╝\n\n"
USERNAME = "@LOSTED_EVERx\n"
LINE = "───────────────────\n"

# --- MAIN MENU (With Buttons) ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    btn_tg = InlineKeyboardButton("🔍 TG ID INFO", callback_data="check_tg")
    btn_num = InlineKeyboardButton("📞 NUMBER SCAN", callback_data="check_num")
    markup.add(btn_tg)
    markup.add(btn_num)
    
    # Hum yahan parse_mode nahi use kar rahe taaki error na aaye
    welcome_text = (
        f"{HEADER}"
        f"💀 System Activated 💀\n"
        f"Bot is Running 24/7!\n"
        f"{LINE}"
        f"Select an operation:\n"
        f"{USERNAME}"
    )
    
    bot.send_message(
        message.chat.id, 
        welcome_text, 
        reply_markup=markup
    )

# --- BUTTON CALLBACKS ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "check_tg":
        bot.send_message(
            call.message.chat.id, 
            "🔍 [TG ID INFO]\nPlease send the Telegram User ID:", 
            reply_markup=ForceReply()
        )
    elif call.data == "check_num":
        bot.send_message(
            call.message.chat.id, 
            "📞 [NUMBER SCAN]\nPlease send the Mobile Number (with country code):", 
            reply_markup=ForceReply()
        )

# --- RESPONSE HANDLER ---
@bot.message_handler(func=lambda message: True)
def handle_replies(message):
    if message.reply_to_message:
        text = message.reply_to_message.text
        
        # Telegram ID Search
        if "Telegram User ID" in text:
            target_id = message.text
            bot.send_message(message.chat.id, f"Searching for ID: {target_id}...")
            url = f"https://tg-2-num-api-org.vercel.app/api/search?userid={target_id}"
            try:
                res = requests.get(url).text
                bot.send_message(message.chat.id, f"{HEADER}{LINE}{res}\n{LINE}{USERNAME}")
            except:
                bot.send_message(message.chat.id, "Error fetching data from API.")
            
        # Mobile Number Search
        elif "Mobile Number" in text:
            target_num = message.text
            bot.send_message(message.chat.id, f"Scanning Number: {target_num}...")
            url = f"https://yash-code-with-ai.alphamovies.workers.dev/?num={target_num}&key=7189814021"
            try:
                res = requests.get(url).text
                bot.send_message(message.chat.id, f"{HEADER}{LINE}{res}\n{LINE}{USERNAME}")
            except:
                bot.send_message(message.chat.id, "Error scanning number.")

# --- START BOT ---
if __name__ == "__main__":
    keep_alive()
    print("Bot is starting...")
    bot.infinity_polling()
