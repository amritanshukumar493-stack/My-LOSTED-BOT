import telebot
import requests
import os
from telebot import types
from threading import Thread
from flask import Flask

# --- CONFIGURATION ---
API_TOKEN = '8727697765:AAHlJVf2_wVzBu-6Et4hZPZcruKqZuY9P4U'
CHANNEL_ID = '@hackedanurag'
BOT_NAME = "⬎̸ 𝐋𝚶𝛅𝚻𝚬𝐃 𝚬𝐕𝚬𝐑𝚼𝚻𝚮𝚰𝚴𝐆 ❜ ⚚"

bot = telebot.TeleBot(API_TOKEN)
app = Flask('')

# --- APIS ---
TG_API = "https://tg-2-num-api-org.vercel.app/api/search?userid="
NUM_API = "https://yash-code-with-ai.alphamovies.workers.dev/?num={}&key=7189814021"

@app.route('/')
def home():
    return "Bot is Running"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

def check_sub(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return True

# --- MAIN LOGIC ---

@bot.message_handler(commands=['start', 'tg', 'num'])
def main_handler(message):
    if not check_sub(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_ID[1:]}"))
        bot.reply_to(message, "⚠️ **Access Denied!**\nPehle channel join karo.", reply_markup=markup)
        return

    # Stylish Buttons for GC and Private
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🔍 TG SEARCH", callback_data="tg_ask")
    btn2 = types.InlineKeyboardButton("📞 NUM SEARCH", callback_data="num_ask")
    markup.add(btn1, btn2)

    text = (f"✨ **{BOT_NAME}**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"Bhai, kya nikalna hai aaj? Niche buttons use kar:")
    bot.reply_to(message, text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "tg_ask":
        bot.answer_callback_query(call.id)
        msg = bot.send_message(call.message.chat.id, "👤 **Reply to this message with TG ID or Username:**", 
                               reply_markup=types.ForceReply(selective=True))
        bot.register_next_step_handler(msg, process_tg)
    
    elif call.data == "num_ask":
        bot.answer_callback_query(call.id)
        msg = bot.send_message(call.message.chat.id, "📱 **Reply to this message with Mobile Number:**", 
                               reply_markup=types.ForceReply(selective=True))
        bot.register_next_step_handler(msg, process_num)

def process_tg(message):
    query = message.text.replace('@', '').strip()
    wait = bot.reply_to(message, "🔄 **Searching TG Database...**")
    try:
        res = requests.get(TG_API + query).json()
        if res.get("status") and res.get("data"):
            d = res["data"]
            bot.edit_message_text(f"⬎̸ 𝐋𝚶𝛅𝚻𝚬𝐃 𝐓𝐆 𝐈𝚴𝐅𝐎 ❜ ⚡\n━━━━━━━━━━━━━\n🆔 **ID:** `{d.get('id')}`\n👤 **Name:** `{d.get('first_name')}`\n🏷 **User:** @{d.get('username')}\n📞 **Phone:** `{d.get('phone')}`\n━━━━━━━━━━━━━", 
                                  message.chat.id, wait.message_id, parse_mode="Markdown")
        else:
            bot.edit_message_text("❌ No data found.", message.chat.id, wait.message_id)
    except:
        bot.edit_message_text("❌ API Error.", message.chat.id, wait.message_id)

def process_num(message):
    num = message.text.strip()
    wait = bot.reply_to(message, "🔄 **Scanning Number...**")
    try:
        res = requests.get(NUM_API.format(num)).json()
        if res.get("status") and res.get("data"):
            u = res["data"][0]
            bot.edit_message_text(f"⬎̸ 𝐋𝚶𝛅𝚻𝚬𝐃 𝚴𝐔𝐌 𝐈𝚴𝐅𝐎 ❜ 🕵️\n━━━━━━━━━━━━━\n👤 **Name:** `{u.get('name')}`\n👨‍🍼 **Father:** `{u.get('father_name')}`\n🏠 **Address:** `{u.get('address')}`\n📱 **Mobile:** `{u.get('mobile')}`\n━━━━━━━━━━━━━", 
                                  message.chat.id, wait.message_id, parse_mode="Markdown")
        else:
            bot.edit_message_text("❌ Number not found.", message.chat.id, wait.message_id)
    except:
        bot.edit_message_text("❌ API Error.", message.chat.id, wait.message_id)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.infinity_polling()
        
