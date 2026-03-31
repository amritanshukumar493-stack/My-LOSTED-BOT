import telebot
import requests
import os
from telebot import types
from threading import Thread
from flask import Flask

# --- CONFIGURATION ---
API_TOKEN = '8768167829:AAFuCKoD8_TMkg8Wk_KsNfrsy10RiD-d4dI'
CHANNEL_ID = '@hackedanurag'
OWNER_ID = 8074231185
BOT_NAME = "⬎̸ 𝐋𝚶𝛅𝚻𝚬𝐃 𝚬𝐕𝚬𝐑𝚼𝚻𝚮𝚰𝚴𝐆 ❜ ⚚"

bot = telebot.TeleBot(API_TOKEN)
app = Flask('')

# --- APIS ---
TG_API = "https://tg-2-num-api-org.vercel.app/api/search?userid="
NUM_API = "https://yash-code-with-ai.alphamovies.workers.dev/?num={}&key=7189814021"

@app.route('/')
def home():
    return "Bot is Running 24/7"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_ID[1:]}")
        markup.add(btn)
        bot.send_message(message.chat.id, f"⚠️ **Access Denied!**\n\nPehle {CHANNEL_ID} join kar tabhi chalega.", reply_markup=markup, parse_mode="Markdown")
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🔍 TG SEARCH", callback_data="tg_info")
    btn2 = types.InlineKeyboardButton("📞 NUM SEARCH", callback_data="num_info")
    markup.add(btn1, btn2)
    
    welcome = (f"✨ **{BOT_NAME}**\n"
               f"━━━━━━━━━━━━━━━━━━━━\n"
               f"Welcome! Main ID aur Number dono nikal sakta hoon.\n\n"
               f"Choose an option below:")
    bot.send_message(message.chat.id, welcome, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "tg_info":
        msg = bot.send_message(call.message.chat.id, "👤 **Enter Telegram ID or Username:**")
        bot.register_next_step_handler(msg, get_tg_info)
    elif call.data == "num_info":
        msg = bot.send_message(call.message.chat.id, "📱 **Enter Mobile Number (With Code):**")
        bot.register_next_step_handler(msg, get_num_info)

def get_tg_info(message):
    query = message.text
    wait = bot.send_message(message.chat.id, "🔄 **Fetching TG Data...**")
    try:
        res = requests.get(TG_API + query).json()
        if res.get("status"):
            data = res.get("data", {})
            text = (f"⬎̸ 𝐋𝚶𝛅𝚻𝚬𝐃 𝐓𝐆 𝐈𝚴𝐅𝐎 ❜ ⚡\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"🆔 **User ID:** `{data.get('id')}`\n"
                    f"👤 **Name:** `{data.get('first_name')}`\n"
                    f"🏷 **Username:** @{data.get('username')}\n"
                    f"📞 **Linked Num:** `{data.get('phone')}`\n"
                    f"━━━━━━━━━━━━━━━━━━━")
            bot.edit_message_text(text, message.chat.id, wait.message_id, parse_mode="Markdown")
        else:
            bot.edit_message_text("❌ No data found for this ID.", message.chat.id, wait.message_id)
    except:
        bot.edit_message_text("❌ API Error or Invalid ID.", message.chat.id, wait.message_id)

def get_num_info(message):
    num = message.text
    wait = bot.send_message(message.chat.id, "🔄 **Scanning Database...**")
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
            bot.edit_message_text("❌ Number not found in database.", message.chat.id, wait.message_id)
    except:
        bot.edit_message_text("❌ API Server Error.", message.chat.id, wait.message_id)

if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    print("Bot is Starting...")
    bot.infinity_polling()
        
