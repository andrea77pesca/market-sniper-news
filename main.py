
from flask import Flask, request
from telegram import constants
from telegram.ext import ApplicationBuilder
import asyncio

app = Flask(__name__)

TOKEN = '7581634970:AAHrZQk3lk7BrnE8osK3vgDfAmMv0f73Q-M'
CHAT_ID = '6288178602'

app_telegram = ApplicationBuilder().token(TOKEN).build()

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'message' in data:
        text = data['message']
        try:
            asyncio.run(app_telegram.bot.send_message(chat_id=CHAT_ID, text=text, parse_mode=constants.ParseMode.HTML))
            return 'Messaggio inviato ✅', 200
        except Exception as e:
            return f"Errore nell'invio: {str(e)}", 500
    return 'Dati non validi ❌', 400

@app.route('/', methods=['GET'])
def home():
    return '🚀 MarketSniper Webhook attivo su Render!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
