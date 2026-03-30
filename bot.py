import telebot
import requests
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply

# --- WEB SERVER (For Render 24/7) ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is Alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOT CONFIGURATION ---
# @BotFather se mila TOKEN yahan dalein
API_TOKEN = '8768167829:AAFlWONi10gcAG-m-V7yrDXOcLLQ1zPWo_s' 
bot = telebot.TeleBot(API_TOKEN)

# --- ANIMATION & LOGO (Stylish) ---
# Yahan apni pasand ki hacker GIF ka URL dalein
HACKER_GIF = "https://media.giphy.com/media/V4NSRHKXhO6Xj96S-e/giphy.gif"

# Stylish Header & Username
HEADER = "╔════════════════╗\n     ⬎̸ 𝐋𝚶𝛅𝚻𝚬𝐃 𝚬𝐕𝚬𝐑𝚼𝚻𝚮𝚰𝚴𝐆 ❜ ⚚🏴‍☠️\n╚════════════════╝\n\n"
USERNAME = "@LOSTED_EVERx\n"
LINE = "───────────────────\n"

# --- STYLISH START MENU (With Animation) ---
@bot.message_handler(commands=['start'])
def start(message):
    # Inline Buttons Banayein
    markup = InlineKeyboardMarkup()
    btn_tg = InlineKeyboardButton("🔍 TG ID INFO", callback_data="check_tg")
    btn_num = InlineKeyboardButton("📞 NUMBER SCAN", callback_data="check_num")
    markup.add(btn_tg)
    markup.add(btn_num) # Buttons ko alag-alag lines mein rakha taaki aur stylish lage
    
    welcome_text = (
        f"{HEADER}"
        f"💀 **Activate System** 💀\n"
        f"Bot is Running 24/7! (Hosted on Render)\n"
        f"{LINE}"
        f"Select an operation:\n"
        f"{USERNAME}"
    )
    
    # Animation bhejte hain pehle, fir uske caption mein welcome message aur buttons
    try:
        bot.send_animation(
            message.chat.id, 
            animation=HACKER_GIF, 
            caption=welcome_text, 
            parse_mode="Markdown", 
            reply_markup=markup
        )
    except Exception as e:
        # Agar GIF fail ho jaye, to normal message bhej dein
        bot.send_message(
            message.chat.id, 
            welcome_text, 
            parse_mode="Markdown", 
            reply_markup=markup
        )

# --- BUTTON CLICK HANDLER (With ForceReply) ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # User ko click par reply karne ke liye "force" karte hain
    if call.data == "check_tg":
        bot.send_message(
            call.message.chat.id, 
            "┌─── 🔍 **TG ID INFO** ───┐\n│ Please send the **Telegram User ID**:", 
            parse_mode="Markdown",
            reply_markup=ForceReply()
        )
    elif call.data == "check_num":
        bot.send_message(
            call.message.chat.id, 
            "┌─── 📞 **NUMBER SCAN** ───┐\n│ Please send the **Mobile Number**:", 
            parse_mode="Markdown",
            reply_markup=ForceReply()
        )

# --- RESPONSE HANDLER (Forces user reply) ---
@bot.message_handler(func=lambda message: True)
def handle_replies(message):
    if message.reply_to_message:
        text = message.reply_to_message.text
        
        if "Telegram User ID" in text:
            target_id = message.text
            bot.send_message(message.chat.id, f"🔍 Searching for Telegram ID: `{target_id}`...", parse_mode="Markdown")
            
            # Aapka real API connection
            url = f"https://tg-2-num-api-org.vercel.app/api/search?userid={target_id}"
            res = requests.get(url).text
            
            bot.send_message(
                message.chat.id, 
                f"{HEADER}{LINE}{res}\n{LINE}{USERNAME}",
                parse_mode="Markdown"
            )
            
        elif "Mobile Number" in text:
            target_num = message.text
            bot.send_message(message.chat.id, f"📞 Scanning Mobile Number: `{target_num}`...", parse_mode="Markdown")
            
            # Aapka real API connection
            url = f"https://yash-code-with-ai.alphamovies.workers.dev/?num={target_num}&key=7189814021"
            res = requests.get(url).text
            
            bot.send_message(
                message.chat.id, 
                f"{HEADER}{LINE}{res}\n{LINE}{USERNAME}",
                parse_mode="Markdown"
            )

# --- START BOT ---
if __name__ == "__main__":
    keep_alive() # Web server starts first
    print("Bot is starting...")
    bot.infinity_polling()
            
