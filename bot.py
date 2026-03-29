import telebot
from telebot import types
import requests

# --- CONFIGURATION ---
API_TOKEN = '8768167829:AAFlWONi10gcAG-m-V7yrDXOcLLQ1zPWo_s'
ADMIN_ID = '8074231185'
bot = telebot.TeleBot(API_TOKEN)

HEADER = "⬎̸ 𝐋𝚶𝛅𝚻𝚬𝐃 𝚬𝐕𝚬𝐑𝚼𝚻𝚮𝚰𝚴𝐆 ❜ ⚚\n"
USERNAME = "@LOSTED_EVERx\n"
LINE = "───────────────────\n"

def send_log(user, command, target):
    log = f"🚀 **LOG**\nUser: {user.first_name}\nID: {user.id}\nAction: {command}\nTarget: {target}"
    try: bot.send_message(ADMIN_ID, log)
    except: pass

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🔍 TG Search", callback_data="help_tg")
    btn2 = types.InlineKeyboardButton("📞 Num Scan", callback_data="help_num")
    btn3 = types.InlineKeyboardButton("💀 Channel", url="https://t.me/LOSTED_EVERx")
    markup.add(btn1, btn2, btn3)
    
    welcome = f"{HEADER}{USERNAME}{LINE}Welcome Bhooms! Select a service below:[span_0](end_span)"
    bot.send_message(message.chat.id, welcome, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "help_tg":
        bot.answer_callback_query(call.id, "Use: /tg [ID]")
    elif call.data == "help_num":
        bot.answer_callback_query(call.id, "Use: /num [Number]")

@bot.message_handler(commands=['tg'])
def tg_info(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "❌ Format: `/tg 12345678`", parse_mode="Markdown")
        return
    
    target_id = args[1]
    send_log(message.from_user, "/tg", target_id)
    bot.send_message(message.chat.id, "📡 **Accessing Database...**", parse_mode="Markdown")
    
    try:
        url = f"https://tg-2-num-api-org.vercel.app/api/search?userid={target_id}"
        res = requests.get(url).text
        bot.send_message(message.chat.id, f"{HEADER}{LINE}TARGET: `{target_id}`\n\n{res}\n{LINE}{USERNAME}")
    except:
        bot.reply_to(message, "⚠️ API Error")

@bot.message_handler(commands=['num'])
def num_info(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "❌ Format: `/num 91xxx`", parse_mode="Markdown")
        return
    
    target_num = args[1]
    send_log(message.from_user, "/num", target_num)
    bot.send_message(message.chat.id, "⚡ **Scanning Network...**", parse_mode="Markdown")
    
    try:
        url = f"https://yash-code-with-ai.alphamovies.workers.dev/?num={target_num}&key=7189814021"
        res = requests.get(url).text
        bot.send_message(message.chat.id, f"{HEADER}{LINE}TARGET: `{target_num}`\n\n{res}\n{LINE}{USERNAME}")
    except:
        bot.reply_to(message, "⚠️ System Error")

bot.infinity_polling()
  
