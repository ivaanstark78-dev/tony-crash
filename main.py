import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# --- COMANDO PRINCIPAL DE ANÁLISIS ---
async def comando_analizar_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Unimos todos los argumentos en un solo bloque de texto
    texto_completo = " ".join(context.args)
    
    # Buscamos equipos (asumiendo formato "Equipo vs Equipo")
    equipos = re.search(r"([A-Za-z\s]+)\s+vs\s+([A-Za-z\s]+)", texto_completo, re.IGNORECASE)
    
    # Buscamos el momio (el primer número con + o - que aparece)
    momio_match = re.search(r"([+-]\d+)", texto_completo)
    
    if not equipos or not momio_match:
        await update.message.reply_text(
            "❌ No pude procesar el texto. Asegúrate de copiar el formato: 'Argentina vs Cabo Verde' seguido del momio (ej. -589)."
        )
        return

    equipo1 = equipos.group(1).strip()
    equipo2 = equipos.group(2).strip()
    momio = int(momio_match.group(1))
    
    # Convertimos momio americano a decimal
    cuota_decimal = (100 / abs(momio)) + 1 if momio < 0 else (momio / 100) + 1
    
    # Lógica de asesoramiento
    if cuota_decimal < 1.30:
        respuesta = (
            f"📊 Análisis para {equipo1} vs {equipo2}:\n\n"
            f"⚠️ Cuota detectada: {cuota_decimal:.2f}.\n"
            f"💡 **Consejo:** Es una cuota demasiado baja para el riesgo. "
            f"No apuestes al ganador. Busca mercados de 'Handicap' o 'Total de goles' "
            f"para encontrar mayor valor."
        )
    else:
        respuesta = (
            f"📊 Análisis para {equipo1} vs {equipo2}:\n\n"
            f"✅ Cuota detectada: {cuota_decimal:.2f}.\n"
            f"💡 **Consejo:** Esta cuota tiene más margen. Analiza si el favorito "
            f"tiene un historial sólido para asegurar la apuesta."
        )
        
    await update.message.reply_text(respuesta)

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    # Registramos el nuevo comando
    app.add_handler(CommandHandler("analizar_texto", comando_analizar_texto))

    print("--- TONY CRASH: MÓDULO DE ANÁLISIS ACTIVO ---")
    app.run_polling()