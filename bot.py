import telebot
import requests
import os
from telebot import types
from threading import Thread
from flask import Flask

# --- CONFIGURATION ---
API_TOKEN = '8727697765:AAGYQCHnl-Hlw8b0eUwHSDPLv7Lh9lvRJK4'
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

# --- MAIN HANDLERS ---

@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_ID[1:]}")
        markup.add(btn)
        bot.reply_to(message, f"⚠️ **Access Denied!**\n\nPehle {CHANNEL_ID} join karo.", reply_markup=markup, parse_mode="Markdown")
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🔍 TG SEARCH", callback_data="tg_info")
    btn2 = types.InlineKeyboardButton("📞 NUM SEARCH", callback_data="num_info")
    markup.add(btn1, btn2)
    
    bot.reply_to(message, f"✨ **{BOT_NAME}**\n\nChoose an option:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "tg_info":
        msg = bot.send_message(call.message.chat.id, "👤 **Enter Telegram ID or Username:**")
        bot.register_next_step_handler(msg, get_tg_info)
    elif call.data == "num_info":
        msg = bot.send_message(call.message.chat.id, "📱 **Enter Mobile Number (With Code):**")
        bot.register_next_step_handler(msg, get_num_info)

# --- TG INFO LOGIC (FIXED) ---
def get_tg_info(message):
    query = message.text.replace('@', '').strip() # @ hatayega aur extra space bhi
    wait = bot.reply_to(message, "🔄 **Searching TG Database...**")
    try:
        # API hit karega
        response = requests.get(TG_API + query)
        res = response.json()
        
        if res.get("status") and res.get("data"):
            d = res["data"]
            # Formatting stylish result
            text = (f"⬎̸ 𝐋𝚶𝛅𝚻𝚬𝐃 𝐓𝐆 𝐈𝚴𝐅𝐎 ❜ ⚡\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"🆔 **ID:** `{d.get('id', 'N/A')}`\n"
                    f"👤 **Name:** `{d.get('first_name', 'N/A')}`\n"
                    f"🏷 **User:** @{d.get('username', 'None')}\n"
                    f"📞 **Phone:** `{d.get('phone', 'Hidden')}`\n"
                    f"━━━━━━━━━━━━━━━━━━━")
            bot.edit_message_text(text, message.chat.id, wait.message_id, parse_mode="Markdown")
        else:
            bot.edit_message_text("❌ **No data found for this ID/User.**", message.chat.id, wait.message_id, parse_mode="Markdown")
    except Exception as e:
        bot.edit_message_text(f"❌ **API Error:** `{str(e)}`", message.chat.id, wait.message_id, parse_mode="Markdown")

# --- NUM INFO LOGIC ---
def get_num_info(message):
    num = message.text.strip()
    wait = bot.reply_to(message, "🔄 **Scanning Number...**")
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
                    f"━━━━━━━━━━━━━━━━━━━")
            bot.edit_message_text(text, message.chat.id, wait.message_id, parse_mode="Markdown")
        else:
            bot.edit_message_text("❌ **Number not in database.**", message.chat.id, wait.message_id)
    except:
        bot.edit_message_text("❌ **API Server Error.**", message.chat.id, wait.message_id)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    print("Bot is Running...")
    bot.infinity_polling()
    
