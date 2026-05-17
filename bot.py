import telebot
from datetime import datetime

TOKEN = "8414397384:AAHashCghQ0tc0XKZFrggZ8cGgdQ6VuPihY"
bot = telebot.TeleBot(TOKEN)

TUBES_PER_PALLET = 1560

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 
        "Пришли скорость в тубах/мин, например: 19")

@bot.message_handler(func=lambda m: True)
def calc(message):
    try:
        speed = float(message.text)
        now = datetime.now()
        stop = now.replace(hour=19, minute=0, second=0, microsecond=0)
        
        if now >= stop:
            bot.reply_to(message, "⚠️ Уже 19:00, станок остановлен")
            return
        
        minutes_left = (stop - now).total_seconds() / 60
        tubes_total = int(speed * minutes_left)
        pallets = tubes_total // TUBES_PER_PALLET
        remaining = tubes_total % TUBES_PER_PALLET
        
        reply = f"📦 {pallets} поддонов\n"
        reply += f"🔧 Остаток туб: {remaining}\n"
        reply += f"⏱ Осталось {round(minutes_left)} мин до 19:00"
        bot.reply_to(message, reply)
    except:
        bot.reply_to(message, "❌ Пришли число, например: 19")

bot.infinity_polling()