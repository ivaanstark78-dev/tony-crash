from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# --- IMPORTA AQUÍ TUS MÓDULOS ---
# from analizador import Analizador 
# analizador = Analizador()

async def comando_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tony Crash iniciado. Escribe /valor [cuota] [probabilidad] para analizar una apuesta.")

# --- NUEVA FUNCIÓN DE VALOR ---
async def comando_valor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # El usuario escribe /valor [cuota] [probabilidad]
        cuota = float(context.args[0])
        probabilidad = float(context.args[1])
        
        # Fórmula de Valor Esperado (EV)
        ev = (probabilidad * cuota) - 1
        porcentaje = ev * 100
        
        if ev > 0:
            resultado = f"✅ ¡TIENE VALOR! EV: {porcentaje:.2f}%. Esta apuesta es matemáticamente rentable."
        else:
            resultado = f"❌ SIN VALOR. EV: {porcentaje:.2f}%. A largo plazo perderás dinero con esta cuota."
            
        await update.message.reply_text(resultado)
    except (IndexError, ValueError):
        await update.message.reply_text("Uso correcto: /valor [cuota] [probabilidad]\nEjemplo: /valor 1.85 0.60")

if __name__ == '__main__':
    # Obtén tu token de las variables de entorno
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    # --- REGISTRO DE COMANDOS ---
    app.add_handler(CommandHandler("start", comando_start))
    app.add_handler(CommandHandler("valor", comando_valor))
    # Aquí irían tus otros comandos como /mx, /mundial, etc.

    print("--- TONY CRASH INICIADO ---")
    app.run_polling()