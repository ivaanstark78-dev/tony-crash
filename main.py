import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

GOOGLE_URL = "https://script.google.com/macros/s/AKfycbz3G-vW5VGsXTcseMcYuUuhSoEY7UOaKBfCglArc8-p46SAQ-oWHDLwuNaInq1KiOHyTw/exec"

async def analizar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Formato esperado: /analizar Mercado Cuota
    if len(context.args) < 2:
        await update.message.reply_text("Usa: /analizar NombreCuota 1.80")
        return
    
    payload = {'mercado': context.args[0], 'cuota': context.args[1]}
    requests.post(GOOGLE_URL, json=payload)
    await update.message.reply_text(f"✅ Apuesta {context.args[0]} registrada en tu base de datos.")

app = ApplicationBuilder().token("TU_TOKEN_AQUI").build()
app.add_handler(CommandHandler("analizar", analizar))
app.run_polling()