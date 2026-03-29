import telebot
import requests
from flask import Flask
from threading import Thread

# --- WEB SERVER FOR 24/7 ---
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
API_TOKEN = '8768167829:AAFlWONi10gcAG-m-V7yrDXOcLLQ1zPWo_s' # Apna Token Dalein
ADMIN_ID = '8074231185'    # Apni ID Dalein
bot = telebot.TeleBot(API_TOKEN)

HEADER = "⬎̸ 𝐋𝚶𝛅𝚻𝚬𝐃 𝚬𝐕𝚬𝐑𝚼𝚻𝚮𝚰𝚴𝐆 ❜ ⚚🏴‍☠️\n"
USERNAME = "@LOSTED_EVERx\n"
LINE = "───────────────────\n"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f"{HEADER}{USERNAME}{LINE}Bot is Running 24/7! 💀")

@bot.message_handler(commands=['tg'])
def tg_info(message):
    args = message.text.split()
    if len(args) < 2: return
    target_id = args[1]
    url = f"https://tg-2-num-api-org.vercel.app/api/search?userid={target_id}"
    res = requests.get(url).text
    bot.send_message(message.chat.id, f"{HEADER}{LINE}{res}\n{LINE}{USERNAME}")

@bot.message_handler(commands=['num'])
def num_info(message):
    args = message.text.split()
    if len(args) < 2: return
    target_num = args[1]
    url = f"https://yash-code-with-ai.alphamovies.workers.dev/?num={target_num}&key=7189814021"
    res = requests.get(url).text
    bot.send_message(message.chat.id, f"{HEADER}{LINE}{res}\n{LINE}{USERNAME}")

# --- START BOT ---
if __name__ == "__main__":
    keep_alive() # Isse web server start hoga
    print("Bot started...")
    bot.infinity_polling()
