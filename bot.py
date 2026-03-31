import telebot
import requests
import os
from telebot import types
from threading import Thread
from flask import Flask

# --- CONFIGURATION ---
API_TOKEN = '8727697765:AAGsFKLIlv06gfIQGvihwtn4Thj3S3HanCk'
CHANNEL_ID = '@hackedanurag'
BOT_NAME = "⬎̸ 𝐋𝚶𝛅𝚻𝚬𝐃 𝚬𝐕𝚬𝐑𝚼𝚻𝚮𝚰𝚴𝐆 ❜ ⚚"

bot = telebot.TeleBot(API_TOKEN)
app = Flask('')

# --- APIS ---
TG_API = "https://tg-2-num-api-org.vercel.app/api/search?userid="
NUM_API = "https://yash-code-with-ai.alphamovies.workers.dev/?num={}&key=7189814021"

@app.route('/')
def home():
    return "Bot is Active 24/7"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return True 

# --- HANDLERS ---

@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_ID[1:]}")
        markup.add(btn)
        bot.reply_to(message, f"⚠️ **Access Denied!**\n\nPehle {CHANNEL_ID} join karo tabhi access milega.", reply_markup=markup, parse_mode="Markdown")
        return

    welcome = (f"✨ **{BOT_NAME}**\n"
               f"━━━━━━━━━━━━━━━━━━━━\n"
               f"Welcome! Use these commands in GC or Private:\n\n"
               f"🔍 `/tg` - For Telegram Search\n"
               f"📞 `/num` - For Number Search")
    bot.reply_to(message, welcome, parse_mode="Markdown")

@bot.message_handler(commands=['tg', 'num'])
def handle_commands(message):
    if not is_subscribed(message.from_user.id): return

    cmd = message.text.split()[0][1:] # 'tg' or 'num'
    markup = types.InlineKeyboardMarkup()
    
    if cmd == 'tg':
        btn = types.InlineKeyboardButton("🔍 SEARCH TG ID", callback_data="tg_info")
        text = "👤 **Telegram Info nikalne ke liye niche click karein:**"
    else:
        btn = types.InlineKeyboardButton("📞 SEARCH NUMBER", callback_data="num_info")
        text = "📱 **Mobile Number scan karne ke liye niche click karein:**"
    
    markup.add(btn)
    bot.reply_to(message, text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "tg_info":
        msg = bot.send_message(call.message.chat.id, "👤 **Enter Telegram ID or Username:**")
        bot.register_next_step_handler(msg, get_tg_info)
    elif call.data == "num_info":
        msg = bot.send_message(call.message.chat.id, "📱 **Enter Mobile Number (With Code):**")
        bot.register_next_step_handler(msg, get_num_info)

def get_tg_info(message):
    query = message.text.replace('@', '')
    wait = bot.reply_to(message, "🔄 **Fetching TG Data...**")
    try:
        res = requests.get(TG_API + query).json()
        if res.get("status") and res.get("data"):
            d = res["data"]
            text = (f"⬎̸ 𝐋𝚶𝛅𝚻𝚬𝐃 𝐓𝐆 𝐈𝚴𝐅𝐎 ❜ ⚡\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"🆔 **ID:** `{d.get('id')}`\n"
                    f"👤 **Name:** `{d.get('first_name')}`\n"
                    f"🏷 **User:** @{d.get('username')}\n"
                    f"📞 **Phone:** `{d.get('phone')}`\n"
                    f"━━━━━━━━━━━━━━━━━━━")
            bot.edit_message_text(text, message.chat.id, wait.message_id, parse_mode="Markdown")
        else:
            bot.edit_message_text("❌ No data found for this ID.", message.chat.id, wait.message_id)
    except:
        bot.edit_message_text("❌ API Error.", message.chat.id, wait.message_id)

def get_num_info(message):
    num = message.text
    wait = bot.reply_to(message, "🔄 **Scanning Database...**")
    try:
        res = requests.get(NUM_API.format(num)).json()
        if res.get("status") and res.get("data"):
            u = res["data"][0]
            text = (f"⬎̸ 𝐋𝚶𝛅𝚻𝚬𝐃 𝚴𝐔𝐌 𝐈𝚴𝐅𝐎 ❜ 🕵️\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"👤 **Name:** `{u.get('name')}`\n"
                    f"👨‍🍼 **Father:** `{u.get('father_name')}`\n"
                    f"🏠 **Address:** `{u.get('address')}`\n"
                    f"📱 **Mobile:** `{u.get('mobile')}`\n"
                    f"📍 **Pincode:** `{u.get('pincode')}`\n"
                    f"━━━━━━━━━━━━━━━━━━━")
            bot.edit_message_text(text, message.chat.id, wait.message_id, parse_mode="Markdown")
        else:
            bot.edit_message_text("❌ Data not found.", message.chat.id, wait.message_id)
    except:
        bot.edit_message_text("❌ API Server Error.", message.chat.id, wait.message_id)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    print("Bot is Starting...")
    bot.infinity_polling()
        
