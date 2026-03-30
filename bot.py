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

# --- CONFIGURATION (APKA DATA SET KAR DIYA HAI) ---
API_TOKEN = '8768167829:AAFuCKoD8_TMkg8Wk_KsNfrsy10RiD-d4dI' 
ADMIN_ID = '8074231185'    
CHANNEL_ID = '@hackedanurag' 
bot = telebot.TeleBot(API_TOKEN, threaded=False)

HEADER = "╔════════════════╗\n     LOSTED EVERYTHING ❜ ⚚🏴‍☠️\n╚════════════════╝\n\n"
USERNAME = "@LOSTED_EVERx\n"
LINE = "───────────────────\n"

# --- FUNCTION: CHECK JOIN ---
def is_user_joined(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        else:
            return False
    except:
        return True 

# --- START COMMAND ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    
    # Admin Alert (Aapko message aayega jab koi bot start karega)
    try:
        bot.send_message(ADMIN_ID, f"🚀 **New Target:** {message.from_user.first_name}\n🆔 `{user_id}`", parse_mode="Markdown")
    except: pass

    # Force Join Check
    if not is_user_joined(user_id):
        markup = InlineKeyboardMarkup()
        btn_join = InlineKeyboardButton("📢 JOIN GROUP", url="https://t.me/hackedanurag")
        btn_verify = InlineKeyboardButton("✅ VERIFY / RESTART", callback_data="start_verify")
        markup.add(btn_join)
        markup.add(btn_verify)
        
        bot.send_message(
            message.chat.id, 
            f"⚠️ **Access Denied!**\n\nYou must join our group to use this bot.\n\nJoin here: {CHANNEL_ID}", 
            reply_markup=markup,
            parse_mode="Markdown"
        )
        return

    # Main Menu
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🤖 CHAT GPT (AI)", callback_data="chat_ai"),
        InlineKeyboardButton("🚗 VEHICLE INFO", callback_data="vahan"),
        InlineKeyboardButton("🆔 AADHAR INFO", callback_data="aadhar"),
        InlineKeyboardButton("🔍 TG ID INFO", callback_data="check_tg"),
        InlineKeyboardButton("📞 NUMBER SCAN", callback_data="check_num"),
        InlineKeyboardButton("🔥 ROAST", callback_data="roast_me"),
        InlineKeyboardButton("💬 OUR GROUP", url="https://t.me/hackedanurag")
    )
    
    bot.send_message(message.chat.id, f"{HEADER}💀 Welcome, Agent {message.from_user.first_name}!\nSystem is Armed.\n{LINE}Select a Tool:", reply_markup=markup)

# --- CALLBACKS ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if not is_user_joined(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Join Group First!", show_alert=True)
        return

    if call.data == "start_verify":
        start(call.message)
    elif call.data == "chat_ai":
        bot.send_message(call.message.chat.id, "🤖 **I am LOSTED-GPT.** Ask me anything:", reply_markup=ForceReply())
    elif call.data == "vahan":
        bot.send_message(call.message.chat.id, "🚗 Enter Vehicle Number (e.g. UP53AL1234):", reply_markup=ForceReply())
    elif call.data == "aadhar":
        bot.send_message(call.message.chat.id, "🆔 Enter Aadhar Number to Search:", reply_markup=ForceReply())
    elif call.data == "check_tg":
        bot.send_message(call.message.chat.id, "🔍 Send Telegram ID:", reply_markup=ForceReply())
    elif call.data == "check_num":
        bot.send_message(call.message.chat.id, "📞 Send Mobile Number:", reply_markup=ForceReply())
    elif call.data == "roast_me":
        roasts = ["Aapki IQ aur phone ki battery, dono single digit mein hain.", "Mirror bhi aapko dekh ke 'Broken Link' dikhata hai."]
        bot.answer_callback_query(call.id, random.choice(roasts), show_alert=True)

# --- RESPONSE HANDLER ---
@bot.message_handler(func=lambda message: True)
def handle_replies(message):
    if not is_user_joined(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Please join the group first!")
        return

    if message.reply_to_message:
        text = message.reply_to_message.text
        # AI Answer
        if "Ask me anything" in text:
            ai_res = requests.get(f"https://api.popcat.xyz/chatbot?msg={message.text}").json()
            bot.send_message(message.chat.id, f"🤖 **AI ANSWER:**\n{ai_res['response']}")
        # Vehicle Info
        elif "Vehicle Number" in text:
            res = requests.get(f"https://api.all-metas.workers.dev/vahan?number={message.text}").text
            bot.send_message(message.chat.id, f"{HEADER}{res}\n{USERNAME}")
        # TG ID
        elif "Telegram ID" in text:
            res = requests.get(f"https://tg-2-num-api-org.vercel.app/api/search?userid={message.text}").text
            bot.send_message(message.chat.id, f"{HEADER}{res}\n{USERNAME}")
        # Number Scan
        elif "Mobile Number" in text:
             res = requests.get(f"https://yash-code-with-ai.alphamovies.workers.dev/?num={message.text}&key=7189814021").text
             bot.send_message(message.chat.id, f"{HEADER}{res}\n{USERNAME}")

if __name__ == "__main__":
    keep_alive()
    bot.remove_webhook()
    bot.infinity_polling()
    
