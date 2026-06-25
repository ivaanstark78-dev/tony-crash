import logging
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from analizador import Analizador

# Cargar configuraciones
load_dotenv()
logging.basicConfig(level=logging.INFO)
analizador = Analizador()

# Diccionario de Ligas
LIGAS = {
    "mx": "140",
    "premier": "39",
    "espana": "140",
    "europa": "2",
    "mundial": "1"
}

# Tu ID Personal
MI_ID = "8911212145"

async def start(update, context):
    mensaje = (
        "¡Hola! Soy **Tony Crash**.\n\n"
        "Comandos disponibles:\n"
        "/mx, /premier, /espana, /europa, /mundial"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

async def comando_partidos(update, context):
    comando = update.message.text.replace("/", "").lower()
    league_id = LIGAS.get(comando)
    
    if not league_id:
        await update.message.reply_text("Liga no reconocida.")
        return
    
    partidos = analizador.obtener_partidos(league_id)
    
    # LÍNEA DE DEPURACIÓN: esto aparecerá en los logs de Render
    print(f"DEBUG: Partidos recibidos para {comando}: {partidos}")
    
    if not partidos:
        await update.message.reply_text(f"No hay partidos programados hoy para {comando.upper()}.")
        return
    
    # Crear el mensaje
    mensaje = f"⚽ *Partidos de hoy ({comando.upper()}):*\n\n"
    for p in partidos:
        home = p['teams']['home']['name']
        away = p['teams']['away']['name']
        mensaje += f"🔹 {home} vs {away}\n"
    
    # Enviar al chat privado del usuario (Iván)
    await context.bot.send_message(chat_id=MI_ID, text=mensaje, parse_mode="Markdown")
    
    # Confirmar en el chat actual
    await update.message.reply_text(f"✅ Los datos de {comando.upper()} han sido enviados a tu chat privado.")

if __name__ == "__main__":
    token = os.getenv("TOKEN")
    app = ApplicationBuilder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    for cmd in LIGAS.keys():
        app.add_handler(CommandHandler(cmd, comando_partidos))
        
    print("--- TONY CRASH INICIADO ---")
    app.run_polling()