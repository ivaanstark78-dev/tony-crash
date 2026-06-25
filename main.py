import logging
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from analizador import Analizador

load_dotenv()
logging.basicConfig(level=logging.INFO)
analizador = Analizador()

LIGAS = {"mx": "140", "premier": "39", "espana": "140", "europa": "2", "mundial": "1"}
MI_ID = "8911212145"

async def comando_partidos(update, context):
    comando = update.message.text.replace("/", "").lower()
    league_id = LIGAS.get(comando)
    
    if not league_id:
        await update.message.reply_text("Liga no reconocida.")
        return
    
    partidos = analizador.obtener_partidos(league_id)
    print(f"DEBUG: Partidos recibidos para {comando}: {partidos}")
    
    if not partidos:
        await update.message.reply_text(f"No hay partidos programados hoy para {comando.upper()}.")
        print("DEBUG: Enviado mensaje de 'No hay partidos'")
        return
    
    mensaje = f"⚽ *Partidos de hoy ({comando.upper()}):*\n\n"
    for p in partidos:
        home = p['teams']['home']['name']
        away = p['teams']['away']['name']
        mensaje += f"🔹 {home} vs {away}\n"
    
    print(f"DEBUG: Enviando mensaje al usuario ID: {MI_ID}")
    await context.bot.send_message(chat_id=MI_ID, text=mensaje, parse_mode="Markdown")
    await update.message.reply_text(f"✅ Los datos de {comando.upper()} han sido enviados.")

if __name__ == "__main__":
    token = os.getenv("TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text("Hola!")))
    for cmd in LIGAS.keys():
        app.add_handler(CommandHandler(cmd, comando_partidos))
    print("--- TONY CRASH INICIADO ---")
    app.run_polling()