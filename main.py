import re
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from analizador import Analizador

# Instanciamos el analizador
analizador = Analizador()

async def comando_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Tony Crash activo como Asesor.\n"
        "Envía tus opciones así:\n/analizar_texto Over 1.5 2.65 Under 1.5 1.41 Corner 7 1.90"
    )

async def comando_analizar_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = " ".join(context.args)
    
    # Buscamos el nombre del mercado y su cuota en decimal.
    # Esto detectará patrones como: "Over 1.5 2.65"
    patrones = re.findall(r"([a-zA-Z\s]+)\s+(\d+\.\d+)", texto)
    
    if not patrones:
        await update.message.reply_text(
            "❌ No detecté mercados. Usa: Nombre Cuota (ej: Colombia 3.45)"
        )
        return

    # Limpiamos los datos extraídos
    mercados = [{'nombre': p[0].strip(), 'cuota': float(p[1])} for p in patrones]
    
    # Usamos el analizador para elegir la mejor opción
    mejor, mensaje_base = analizador.seleccionar_mejor_opcion(mercados)
    
    if not mejor:
        await update.message.reply_text(mensaje_base)
        return

    # Estimación de probabilidad (0.85 estándar para este cálculo)
    prob_estimada = 0.85
    
    # Calculamos el stake y le ponemos un TOPE SEGURO de 3.0%
    stake_calculado = analizador.calcular_stake(mejor['cuota'], prob_estimada)
    stake_seguro = min(stake_calculado, 3.0)
    
    respuesta = (
        f"🎯 **Análisis Automático (Tony Crash)**\n\n"
        f"✅ La mejor opción es: **{mejor['nombre']}**\n"
        f"📈 Cuota: {mejor['cuota']:.2f}\n"
        f"💰 **Stake recomendado:** {stake_seguro:.1f}% de tu banca.\n\n"
        f"💡 _Nota: He evaluado {len(mercados)} opción(es). Limitamos el stake a un máximo del 3% para proteger tu capital._"
    )
    
    await update.message.reply_text(respuesta)

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token:
        print("ERROR: El token no está configurado en las variables de entorno.")
    else:
        app = ApplicationBuilder().token(token).build()
        
        app.add_handler(CommandHandler("start", comando_start))
        app.add_handler(CommandHandler("analizar_texto", comando_analizar_texto))
        
        print("--- TONY CRASH: ASESOR DE APUESTAS LISTO ---")
        app.run_polling()