import telebot
import requests
import time
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply

# --- FAST WEB SERVER (For Render 24/7) ---
app = Flask('')
@app.route('/')
def home(): return "LOSTED OSINT BOT IS LIVE"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- CONFIGURATION (NAYA TOKEN SET HAI) ---
API_TOKEN = '8727697765:AAE6qBSs4cOFaRaHXPYizUneIIfn7afWY54' 
ADMIN_ID = '8074231185'
CHANNEL_ID = '@hackedanurag' 
bot = telebot.TeleBot(API_TOKEN, threaded=True)

# --- STYLISH LABELS ---
NAME_TAG = "⬎̸ 𝐋𝚶𝛅𝚻𝚬𝐃 𝚬𝐕𝚬𝐑𝚼𝚻𝚮𝚰𝚴𝐆 ❜ ⚚"
USER_TAG = "@LOSTED_EVERx"
LINE = "───────────────────\n"

# --- CHECK JOIN FUNCTION ---
def is_joined(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except: return True

# --- START COMMAND ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if not is_joined(user_id):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📢 JOIN GROUP", url="https://t.me/hackedanurag"))
        markup.add(InlineKeyboardButton("✅ VERIFY", callback_data="verify"))
        bot.send_message(message.chat.id, f"{NAME_TAG}\n\n⚠️ **Access Denied!**\nJoin @hackedanurag to use this bot.", reply_markup=markup, parse_mode="Markdown")
        return

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔍 TG ID INFO", callback_data="tg"),
        InlineKeyboardButton("📞 NUMBER SCAN", callback_data="num"),
        InlineKeyboardButton("💬 OUR GROUP", url="https://t.me/hackedanurag")
    )
    bot.send_message(message.chat.id, f"{NAME_TAG}\n{USER_TAG}\n\n💀 **Agent Connected!**\nNaya Token Activated. Select tool:", reply_markup=markup)

# --- GC & DM COMMANDS (/tg and /num) ---
@bot.message_handler(commands=['tg', 'num'])
def handle_commands(message):
    if not is_joined(message.from_user.id):
        bot.reply_to(message, "❌ Join @hackedanurag first!")
        return

    markup = InlineKeyboardMarkup()
    if "tg" in message.text:
        markup.add(InlineKeyboardButton("🔍 ENTER TG ID / USERNAME", callback_data="tg"))
        bot.send_message(message.chat.id, f"{NAME_TAG}\nClick to start Telegram Scan:", reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("📞 ENTER MOBILE NUMBER", callback_data="num"))
        bot.send_message(message.chat.id, f"{NAME_TAG}\nClick to start Mobile Scan:", reply_markup=markup)

# --- BUTTONS CALLBACK ---
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "verify": start(call.message)
    elif not is_joined(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Join Group First!", show_alert=True)
        return

    chat_id = call.message.chat.id
    if call.data == "tg":
        bot.send_message(chat_id, "🔍 **TG ID:** Enter ID or Username (Reply to this):", reply_markup=ForceReply(selective=True))
    elif call.data == "num":
        bot.send_message(chat_id, "📞 **Num Scan:** Enter Mobile Number (Reply to this):", reply_markup=ForceReply(selective=True))

# --- MAIN RESPONSE HANDLER ---
@bot.message_handler(func=lambda message: True)
def main_handler(message):
    if not is_joined(message.from_user.id): return
    
    if message.reply_to_message:
        text = message.reply_to_message.text
        
        # TG ID Search Logic
        if "TG ID" in text:
            msg = bot.reply_to(message, "🛰️ *Accessing Telegram Database...*", parse_mode="Markdown")
            try:
                res = requests.get(f"https://tg-2-num-api-org.vercel.app/api/search?userid={message.text}").text
                bot.edit_message_text(f"{NAME_TAG}\n{LINE}{res}\n{LINE}{USER_TAG}", message.chat.id, msg.message_id)
            except: bot.edit_message_text("❌ Database Timeout.", message.chat.id, msg.message_id)

        # Number Scan Logic
        elif "Num Scan" in text:
            msg = bot.reply_to(message, "📡 *Scanning Mobile Records...*", parse_mode="Markdown")
            try:
                res = requests.get(f"https://yash-code-with-ai.alphamovies.workers.dev/?num={message.text}&key=7189814021").text
                bot.edit_message_text(f"{NAME_TAG}\n{LINE}{res}\n{LINE}{USER_TAG}", message.chat.id, msg.message_id)
            except: bot.edit_message_text("❌ Scan Failed.", message.chat.id, msg.message_id)

if __name__ == "__main__":
    keep_alive()
    bot.remove_webhook() # Purane ghost connections khatam karne ke liye
    time.sleep(1)
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
    
