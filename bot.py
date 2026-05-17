import os
import threading
from flask import Flask
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# --- Настройки бота ---
TOKEN = "8878033329:AAGQK7VuAqkv4YQt2J046NkpIbZWYrunkfg" # Токен из переменных окружения
TUBES_PER_PALLET = 1560

# --- Логика бота (ваша функция) ---
async def start(update, context):
    await update.message.reply_text("Бот работает! Отправьте скорость (туб/мин)")

# --- Код, который запускает бота ---
def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    # Здесь добавьте ваш обработчик сообщений
    print("Бот запущен")
    app.run_polling()

# --- Веб-сервер Flask, чтобы Render не убивал процесс ---
flask_app = Flask(__name__)
@flask_app.route('/')
@flask_app.route('/health')
def health():
    return "OK"

if __name__ == "__main__":
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    
    # Запускаем Flask-сервер на порту, который требует Render
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port)