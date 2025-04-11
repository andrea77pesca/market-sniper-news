
import logging
from flask import Flask, request
from telegram import Bot
import asyncio
import os

# === CONFIGURAZIONE ===
TOKEN = '7581634970:AAHrZQk3lk7BrnE8osK3vgDfAmMv0f73Q-M'
CHAT_ID = '6288178602'

# === INIZIALIZZAZIONE ===
app = Flask(__name__)
bot = Bot(token=TOKEN)
logging.basicConfig(level=logging.INFO)

# === FILTRI INTELLIGENTI ===
FILTERS = {
    "fed": "🔍 FED in movimento → monitora @MNQ o @MES. Attendi conferma su volumi.",
    "powell": "📊 Powell in dichiarazione → possibile impatto su @MNQ. Valuta filtro ADX > 30.",
    "rate hike": "📈 Aumento tassi in vista → attento a breakout su @MNQ o ritracciamento @MGC.",
    "gold": "🟡 Oro menzionato → osserva @MGC per segnali long sopra resistenza recente.",
    "silver": "🔘 Argento citato → correlato a @SI. Possibile riflesso anche su @MGC.",
    "oil": "🛢️ Petrolio sotto i riflettori → breakout possibile su @MCL. Verifica media mobile 20.",
    "opec": "🌐 Decisioni OPEC → forte impatto su @MCL. Evita operare prima della conferma direzionale.",
    "russia": "⚠️ Tensione geopolitica (Russia) → rifugio in oro @MGC o rotazione su smallcap @M2K.",
    "china": "🇨🇳 Notizia Cina → monitorare @MGC per riflessi risk-off o @M2K per export USA.",
    "trump": "📰 Trump coinvolto → probabile reazione su @MES. Attendi volumi sopra la media.",
    "nasdaq": "💻 Nasdaq citato → controlla @MNQ. Bias bullish se sopra EMA 50.",
    "dow jones": "🏛️ Dow Jones → impatto su @MYM. Cerca divergenze RSI per conferma ingresso.",
    "s&p": "📉 S&P500 nel titolo → valuta breakout su @MNQ o reversal su @MES.",
    "recession": "🧯 Recessione menzionata → possibile spike di volatilità su @MNQ. Usa trailing stop.",
    "inflation": "📈 Inflazione → valuta short su tech (@MNQ), long su @MGC con supporto confermato."
}

# === WEBHOOK ===
@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data or 'message' not in data:
        return 'Dati non validi ❌', 400

    text = data['message']
    response = [f"📰 {text}"]

    for keyword, reply in FILTERS.items():
        if keyword.lower() in text.lower():
            response.append(reply)

    message = '\n'.join(response)
    try:
        asyncio.run(bot.send_message(chat_id=CHAT_ID, text=message))
        return 'Messaggio inviato ✅', 200
    except Exception as e:
        logging.error(f"Errore invio messaggio: {e}")
        return f'Errore: {str(e)}', 500

# === ROUTE DI TEST ===
@app.route('/', methods=['GET'])
def home():
    return '✅ MarketSniperBot con filtri attivi e suggerimenti operativi!'

# === AVVIO SERVER ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
