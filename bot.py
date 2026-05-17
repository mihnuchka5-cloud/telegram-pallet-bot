import os
import asyncio
import threading
from datetime import datetime
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ========== НАСТРОЙКИ ==========
TOKEN = "8765744061:AAFoaj_K8WCpK9gWd1Jkp__PnrsyjbjUpfg"
TUBES_PER_PALLET = 1560
STOP_HOUR = 19
STOP_MINUTE = 0

# ========== ЛОГИКА БОТА ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📦 Привет! Я считаю, сколько поддонов можно успеть сделать до 19:00.\n\n"
        "Просто отправь мне скорость станка в тубах/мин, например: 19"
    )

async def calculate_pallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        speed = float(update.message.text.strip())
        now = datetime.now()
        stop = now.replace(hour=STOP_HOUR, minute=STOP_MINUTE, second=0, microsecond=0)
        
        if now >= stop:
            await update.message.reply_text("⚠️ Уже 19:00 или позже — станок остановлен")
            return
        
        minutes_left = (stop - now).total_seconds() / 60
        tubes_total = int(speed * minutes_left)
        pallets = tubes_total // TUBES_PER_PALLET
        remaining = tubes_total % TUBES_PER_PALLET
        
        reply = f"📦 **{pallets}** целых поддонов\n"
        reply += f"🔧 Остаток туб: {remaining} из {TUBES_PER_PALLET}\n"
        reply += f"⏱ Осталось {round(minutes_left)} минут до 19:00\n"
        reply += f"🏭 Всего туб успеется: {tubes_total}"
        
        await update.message.reply_text(reply)
        
    except ValueError:
        await update.message.reply_text("❌ Отправь число, например: 19")

def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate_pallets))
    print("🤖 Бот запущен и работает...")
    app.run_polling()

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Бот работает!"

@app.route('/health')
def health():
    return "OK", 200

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)