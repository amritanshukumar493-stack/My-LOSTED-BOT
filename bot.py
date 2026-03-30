import telebot
import requests
import time
import random
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply

# --- WEB SERVER (For Render 24/7) ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is God-Mode Live!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURATION ---
API_TOKEN = '8768167829:AAFuCKoD8_TMkg8Wk_KsNfrsy10RiD-d4dI' 
ADMIN_ID = '8074231185'    
CHANNEL_ID = '@hackedanurag' 
bot = telebot.TeleBot(API_TOKEN, threaded=False)

HEADER = "╔════════════════╗\n     LOSTED EVERYTHING ❜ ⚚\n╚════════════════╝\n\n"
USERNAME = "@LOSTED_EVERx\n"
LINE = "───────────────────\n"

# --- FUNCTION: CHECK JOIN ---
def is_user_joined(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return True 

# --- START COMMAND ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if not is_user_joined(user_id):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📢 JOIN GROUP", url="https://t.me/hackedanurag"))
        markup.add(InlineKeyboardButton("✅ VERIFY", callback_data="start_verify"))
        bot.send_message(message.chat.id, "⚠️ **Access Denied!**\n\nJoin our group first to use the bot.", reply_markup=markup)
        return

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🤖 CHAT GPT", callback_data="chat_ai"),
        InlineKeyboardButton("🚗 VEHICLE INFO", callback_data="vahan"),
        InlineKeyboardButton("🆔 AADHAR INFO", callback_data="aadhar"),
        InlineKeyboardButton("🔍 TG ID", callback_data="check_tg"),
        InlineKeyboardButton("📞 NUMBER SCAN", callback_data="check_num"),
        InlineKeyboardButton("🔥 ROAST", callback_data="roast_me"),
        InlineKeyboardButton("💬 OUR GROUP", url="https://t.me/hackedanurag")
    )
    bot.send_message(message.chat.id, f"{HEADER}💀 Welcome Agent {message.from_user.first_name}!\nSelect a tool:", reply_markup=markup)

# --- CALLBACKS ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "start_verify":
        start(call.message)
    elif call.data == "chat_ai":
        bot.send_message(call.message.chat.id, "🤖 **I am LOSTED-GPT.** Ask me anything:", reply_markup=ForceReply())
    elif call.data == "vahan":
        bot.send_message(call.message.chat.id, "🚗 Enter Vehicle Number (e.g. UP53AL1234):", reply_markup=ForceReply())
    elif call.data == "aadhar":
        bot.send_message(call.message.chat.id, "🆔 Enter Aadhar Number:", reply_markup=ForceReply())
    elif call.data == "check_tg":
        bot.send_message(call.message.chat.id, "🔍 Send Telegram ID:", reply_markup=ForceReply())
    elif call.data == "check_num":
        bot.send_message(call.message.chat.id, "📞 Send Mobile Number:", reply_markup=ForceReply())
    elif call.data == "roast_me":
        roasts = ["IQ aur phone battery dono single digit mein hain.", "Mirror bhi aapko dekh kar 'Connection Failed' bolta hai."]
        bot.answer_callback_query(call.id, random.choice(roasts), show_alert=True)

# --- RESPONSE HANDLER ---
@bot.message_handler(func=lambda message: True)
def handle_replies(message):
    if message.reply_to_message:
        text = message.reply_to_message.text
        
        # 1. NEW STABLE AI CHAT
        if "Ask me anything" in text:
            msg = bot.send_message(message.chat.id, "🤖 *Thinking...*")
            try:
                # Using a different stable API
                api_url = f"https://api.simsimi.net/v2/?text={message.text}&lc=en"
                res = requests.get(api_url, timeout=10).json()
                bot.edit_message_text(f"🤖 **AI:** {res['success']}", message.chat.id, msg.message_id)
            except Exception as e:
                bot.edit_message_text("❌ AI Error: API not responding. Try again.", message.chat.id, msg.message_id)

        # 2. VEHICLE INFO
        elif "Vehicle Number" in text:
            try:
                res = requests.get(f"https://api.all-metas.workers.dev/vahan?number={message.text}", timeout=10).text
                bot.send_message(message.chat.id, f"{HEADER}{res}\n{USERNAME}")
            except:
                bot.send_message(message.chat.id, "❌ Vehicle API error.")

        # 3. TG ID SEARCH
        elif "Telegram ID" in text:
            try:
                res = requests.get(f"https://tg-2-num-api-org.vercel.app/api/search?userid={message.text}", timeout=10).text
                bot.send_message(message.chat.id, f"{HEADER}{res}\n{USERNAME}")
            except:
                bot.send_message(message.chat.id, "❌ TG ID API error.")

if __name__ == "__main__":
    keep_alive()
    bot.remove_webhook()
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
            
