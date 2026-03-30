import telebot
import requests
import time
import random
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply

# --- WEB SERVER (For Render) ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is Ultra-Live!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURATION ---
API_TOKEN = '8768167829:AAFlWONi10gcAG-m-V7yrDXOcLLQ1zPWo_s' # @BotFather wala token
ADMIN_ID = '8074231185'    # @userinfobot wali ID
bot = telebot.TeleBot(API_TOKEN)

HEADER = "╔════════════════╗\n     LOSTED EVERYTHING ❜ ⚚🏴‍☠️\n╚════════════════╝\n\n"
USERNAME = "@LOSTED_EVERx\n"
LINE = "───────────────────\n"

# --- START COMMAND ---
@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    try:
        bot.send_message(ADMIN_ID, f"🚀 New User: {user.first_name} (@{user.username})")
    except: pass

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔍 TG ID", callback_data="check_tg"),
        InlineKeyboardButton("📞 NUMBER", callback_data="check_num"),
        InlineKeyboardButton("🤖 CHAT AI", callback_data="chat_ai"),
        InlineKeyboardButton("🔥 ROAST", callback_data="roast_me"),
        InlineKeyboardButton("💀 HACK SIM", callback_data="hack_sim"),
        InlineKeyboardButton("📍 LOCATION", callback_data="track_loc")
    )
    
    bot.send_message(message.chat.id, f"{HEADER}💀 Welcome {user.first_name}!\nChoose a tool:", reply_markup=markup)

# --- CALLBACKS ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "check_tg":
        bot.send_message(call.message.chat.id, "🔍 Send Telegram ID:", reply_markup=ForceReply())
    elif call.data == "check_num":
        bot.send_message(call.message.chat.id, "📞 Send Mobile Number:", reply_markup=ForceReply())
    elif call.data == "track_loc":
        bot.send_message(call.message.chat.id, "📍 Send IP Address:", reply_markup=ForceReply())
    elif call.data == "hack_sim":
        bot.send_message(call.message.chat.id, "💀 Enter Name to Hack:", reply_markup=ForceReply())
    elif call.data == "chat_ai":
        bot.send_message(call.message.chat.id, "🤖 Send your question to AI:", reply_markup=ForceReply())
    elif call.data == "roast_me":
        roasts = ["Aapki shakal dekh kar network bhag jata hai.", "Dimaag itna slow hai ki 2G bhi sharma jaye.", "Bhagwan dimaag baant rahe the toh aap shayad line mein nahi the."]
        bot.answer_callback_query(call.id, random.choice(roasts), show_alert=True)

# --- RESPONSE HANDLER ---
@bot.message_handler(func=lambda message: True)
def handle_replies(message):
    if message.reply_to_message:
        text = message.reply_to_message.text
        # 1. AI CHAT
        if "question to AI" in text:
            query = message.text
            try:
                # SimSimi API for Hindi/English Chat
                res = requests.get(f"https://api.simsimi.net/v2/?text={query}&lc=hi").json()
                reply = res.get('success', 'Nahi pata bhai!')
                bot.send_message(message.chat.id, f"🤖 **AI:** {reply}")
            except:
                bot.send_message(message.chat.id, "❌ AI Offline.")
        # 2. HACK SIM
        elif "Name to Hack" in text:
            msg = bot.send_message(message.chat.id, "⚡ Hacking Started...")
            time.sleep(1)
            bot.edit_message_text(f"✅ Data Leaked for {message.text}! 💀", message.chat.id, msg.message_id)
        # 3. TG ID SEARCH
        elif "Telegram ID" in text:
            res = requests.get(f"https://tg-2-num-api-org.vercel.app/api/search?userid={message.text}").text
            bot.send_message(message.chat.id, f"{HEADER}{res}\n{USERNAME}")
        # 4. NUMBER SCAN
        elif "Mobile Number" in text:
            res = requests.get(f"https://yash-code-with-ai.alphamovies.workers.dev/?num={message.text}&key=7189814021").text
            bot.send_message(message.chat.id, f"{HEADER}{res}\n{USERNAME}")
        # 5. IP TRACK
        elif "IP Address" in text:
            data = requests.get(f"http://ip-api.com/json/{message.text}").json()
            if data['status'] == 'success':
                res = f"🌍 Location: {data['country']}, {data['city']}\n🛰️ IP: {data['query']}"
                bot.send_message(message.chat.id, f"{HEADER}{res}\n{USERNAME}")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
    
