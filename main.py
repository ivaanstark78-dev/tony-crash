import re
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from analizador import Analizador

# Instanciamos el analizador
analizador = Analizador()

async def comando_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tony Crash activo. Usa /analizar_texto [EquipoA] vs [EquipoB] [momio]")

async def comando_analizar_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_completo = " ".join(context.args)
    
    # Buscamos equipos y momio
    equipos = re.search(r"([A-Za-z\s]+)\s+vs\s+([A-Za-z\s]+)", texto_completo, re.IGNORECASE)
    momio_match = re.search(r"([+-]\d+)", texto_completo)
    
    if not equipos or not momio_match:
        await update.message.reply_text("❌ Formato incorrecto. Usa: /analizar_texto EquipoA vs EquipoB [momio]")
        return

    equipo1 = equipos.group(1).strip()
    equipo2 = equipos.group(2).strip()
    momio = int(momio_match.group(1))
    
    # Conversión a cuota decimal
    cuota = (100 / abs(momio)) + 1 if momio < 0 else (momio / 100) + 1
    
    # Estimación de probabilidad (0.85 estándar para favoritos)
    prob_estimada = 0.85
    
    # Cálculos usando la clase Analizador
    ev = analizador.calcular_valor(cuota, prob_estimada)
    stake = analizador.calcular_stake(cuota, prob_estimada)
    
    respuesta = (
        f"📊 **Análisis para {equipo1} vs {equipo2}**\n\n"
        f"✅ Cuota: {cuota:.2f}\n"
        f"📈 Valor Esperado: {ev:.1f}%\n"
        f"💰 **Stake recomendado:** {stake:.1f}% de tu banca.\n\n"
    )
    
    if stake < 2:
        respuesta += "⚠️ **Consejo:** El valor es mínimo. No es una apuesta recomendada."
    else:
        respuesta += "🚀 **Consejo:** Tiene valor matemático. Mantén el stake bajo control."
        
    await update.message.reply_text(respuesta)

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("ERROR: El token no está configurado en las variables de entorno.")
    else:
        app = ApplicationBuilder().token(token).build()
        app.add_handler(CommandHandler("start", comando_start))
        app.add_handler(CommandHandler("analizar_texto", comando_analizar_texto))
        print("--- TONY CRASH: SISTEMA DE ANÁLISIS LISTO ---")
        app.run_polling()