import logging
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from analizador import Analizador

# Cargar configuraciones
load_dotenv()
logging.basicConfig(level=logging.INFO)
analizador = Analizador()

# Diccionario de Ligas (IDs de API-Sports)
LIGAS = {
    "mx": "140",       # Liga MX
    "premier": "39",   # Premier League
    "espana": "140",   # La Liga (ID puede variar según temporada en API)
    "europa": "2",     # Champions League
    "mundial": "1"     # FIFA World Cup
}

async def comando_partidos(update, context):
    comando = update.message.text.replace("/", "").lower()
    league_id = LIGAS.get(comando)
    
    if not league_id:
        await update.message.reply_text("Liga no reconocida.")
        return
    
    partidos = analizador.obtener_partidos(league_id)
    
    if not partidos:
        await update.message.reply_text(f"No hay partidos programados hoy para {comando.upper()}.")
        return
    
    mensaje = f"⚽ *Partidos de hoy ({comando.upper()}):*\n\n"
    for p in partidos:
        home = p['teams']['home']['name']
        away = p['teams']['away']['name']
        mensaje += f"🔹 {home} vs {away}\n"
    
    await update.message.reply_text(mensaje, parse_mode="Markdown")

if __name__ == "__main__":
    token = os.getenv("TOKEN")
    if not token:
        print("ERROR: El TOKEN de Telegram no está configurado.")
    else:
        app = ApplicationBuilder().token(token).build()
        
        # Registramos todos los comandos
        for cmd in LIGAS.keys():
            app.add_handler(CommandHandler(cmd, comando_partidos))
        
        print("--- TONY CRASH INICIADO ---")
        app.run_polling()