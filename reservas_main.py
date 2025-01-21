from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters,ContextTypes, CallbackQueryHandler, PreCheckoutQueryHandler
import os
from dotenv import load_dotenv
import asyncio

from reservas import GoogleCalendarManager
from datetime import datetime, timedelta
import threading

load_dotenv()

token = os.getenv("TOKEN_API_RESERVAS")
user_name = os.getenv("USER_BOT_RESERVAS")

URL_IG = "https://www.instagram.com/lllit_3/"
MAPS = "https://maps.app.goo.gl/JF7qNA8vXvBfKEu9A"

calendar_manager = GoogleCalendarManager()

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot de Reservas de Mapping está en funcionamiento."

"""
Para setear los comandos aplicar esto en BotFather
/setcommands

"""

# Comandos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    keyboard = [
        [
            InlineKeyboardButton("📖 Reservar", callback_data="reservar"),
            InlineKeyboardButton("🔍 Precios", callback_data="masinformacion"),
            
        ],
        [
            InlineKeyboardButton("🎨 Nuestros Servicios", url=URL_IG)
        ],
        [
            InlineKeyboardButton("⏱️ Horario", callback_data="horario"),
            InlineKeyboardButton("📡 Ubicación", url=MAPS)
        ],
        [
            InlineKeyboardButton("📞 Contacto", callback_data="contacto")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)


    await update.message.reply_text("🖖 Bienvenid@, ¿Que te gustaria hacer?", reply_markup=reply_markup)


# ------ Reservas -----------------
async def reservas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if update.message:
        await update.message.reply_text("Fecha y Hora de Inicio\nFormato: AAAA-MM-DD HH:MM")
    elif update.callback_query:
        await update.callback_query.message.reply_text("Fecha y Hora de Inicio\nFormato: AAAA-MM-DD HH:MM")
    context.user_data['awaiting_start_time'] = True
    print(f"User Data after /reservas: {context.user_data}")  # Debugging line


# ------ Precios + Informacion -------

async def servicios_mapping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    if update.callback_query:
    # Detalles y precios de los servicios de mapping
        servicios = [
            
            {
                "nombre": "Mapping Accesible Normal", 
                "precio": "$60.000", 
                "detalles": "Mapping en estructuras predeterminadas, No live VJ.",
                "Computadora": " Dell, 8Gb Ram, Radeon Graphics AMD, No GPU",
                "Proyector": " No incluye proyector"
            },
            {
                "nombre": "Mapping Accesible Normal + Proyector", 
                "precio": "$110.000", 
                "detalles": "Mapping en estructuras predeterminadas, No live VJ.",
                "Computadora": " Dell, 8Gb Ram, Radeon Graphics AMD, No GPU",
                "Proyector": " Si incluye proyector 4200 Lumenes"
            },
            {
                "nombre": "Mapping Accesible Medium", 
                "precio": "$90.000", 
                "detalles": "Mapping en estructuras predeterminadas, Live VJ.",
                "Computadora": " Lenovo Legion, 24Gb Ram, AMD Ryzen 5 5600H with Radeon Graphics 3.30 GHz, NVIDIA GeForce RTX 3060",
                "Proyector": " No incluye Proyector"
            },
            {
                "nombre": "Mapping Accesible Medium + Proyector", 
                "precio": "$150.000", 
                "detalles": "Mapping en estructuras predeterminadas, Live VJ.",
                "Computadora": " Lenovo Legion, 24Gb Ram, AMD Ryzen 5 5600H with Radeon Graphics 3.30 GHz, NVIDIA GeForce RTX 3060",
                "Proyector": " Si incluye proyector 4200 Lumenes"
            },
            {
                "nombre": "Mapping Personalizado", 
                "precio": "A consultar", 
                "detalles": "Proyección personalizada según las necesidades del cliente.",
                "Computadora": " A consultar",
                "Proyector": " A consultar"
            }
        ]

        texto_servicios = "🖼️ **Nuestros servicios de mapping:**\n\n"

        for servicio in servicios:
            texto_servicios += (
                f"📌 *{servicio['nombre']}*\n"
                f"💲 Precio: {servicio['precio']}\n"
                f"📝 Detalles: {servicio['detalles']}\n"
                f"💻 Computadora: {servicio['Computadora']}\n"
                f"📽️ Proyector: {servicio['Proyector']}\n"
                "--------------------------------\n\n"
            )

        texto_servicios += f"⭕ **Informacion Importarte:** \nCada servicio de mapping incluye un técnico que se encargará de la instalación y ejecución del mapping. El precio no incluye el transporte del técnico ni el transporte de los equipos.\n\n⭕ **Reservas Validas:** \nPara que tu servicio quede 100% reservada, debes realizar el pago del 50% del valor total del servicio. El pago se realiza por transferencia bancaria y el comprobante debe ser enviado al correo\n\n"

        texto_servicios += "\n📞 **Contacto:**\nPara más información o reservas, puedes contactarnos a través de nuestro correo:\nlit.io30303@gmail.com"
        texto_servicios += "\n\n📖 **Reservar:**\nPara reservar, enviar /reservas\n\n"

        await update.callback_query.edit_message_text(text=texto_servicios, parse_mode='Markdown')
    elif update and update.message:
        servicios = [
            
            {
                "nombre": "Mapping Accesible Normal", 
                "precio": "$60.000", 
                "detalles": "Mapping en estructuras predeterminadas, No live VJ.",
                "Computadora": " Dell, 8Gb Ram, Radeon Graphics AMD, No GPU",
                "Proyector": " No incluye proyector"
            },
            {
                "nombre": "Mapping Accesible Normal + Proyector", 
                "precio": "$110.000", 
                "detalles": "Mapping en estructuras predeterminadas, No live VJ.",
                "Computadora": " Dell, 8Gb Ram, Radeon Graphics AMD, No GPU",
                "Proyector": " Si incluye proyector 4200 Lumenes"
            },
            {
                "nombre": "Mapping Accesible Medium", 
                "precio": "$90.000", 
                "detalles": "Mapping en estructuras predeterminadas, Live VJ.",
                "Computadora": " Lenovo Legion, 24Gb Ram, AMD Ryzen 5 5600H with Radeon Graphics 3.30 GHz, NVIDIA GeForce RTX 3060",
                "Proyector": " No incluye Proyector"
            },
            {
                "nombre": "Mapping Accesible Medium + Proyector", 
                "precio": "$150.000", 
                "detalles": "Mapping en estructuras predeterminadas, Live VJ.",
                "Computadora": " Lenovo Legion, 24Gb Ram, AMD Ryzen 5 5600H with Radeon Graphics 3.30 GHz, NVIDIA GeForce RTX 3060",
                "Proyector": " Si incluye proyector 4200 Lumenes"
            },
            {
                "nombre": "Mapping Personalizado", 
                "precio": "A consultar", 
                "detalles": "Proyección personalizada según las necesidades del cliente.",
                "Computadora": " A consultar",
                "Proyector": " A consultar"
            }
        ]

        texto_servicios = "🖼️ **Nuestros servicios de mapping:**\n\n"

        for servicio in servicios:
            texto_servicios += (
                f"📌 *{servicio['nombre']}*\n"
                f"💲 Precio: {servicio['precio']}\n"
                f"📝 Detalles: {servicio['detalles']}\n"
                f"💻 Computadora: {servicio['Computadora']}\n"
                f"📽️ Proyector: {servicio['Proyector']}\n"
                "--------------------------------\n\n"
            )

        texto_servicios += f"⭕ **Informacion Importarte:** \nCada servicio de mapping incluye un técnico que se encargará de la instalación y ejecución del mapping. El precio no incluye el transporte del técnico ni el transporte de los equipos.\n\n⭕ **Reservas Validas:** \nPara que tu servicio quede 100% reservada, debes realizar el pago del 50% del valor total del servicio. El pago se realiza por transferencia bancaria y el comprobante debe ser enviado al correo\n\n"

        texto_servicios += "\n📞 **Contacto:**\nPara más información o reservas, puedes contactarnos a través de nuestro correo:\nlit.io30303@gmail.com"
        texto_servicios += "\n\n📖 **Reservar:**\nPara reservar, enviar /reservas\n\n"

        #await update.callback_query.edit_message_text(text=texto_servicios, parse_mode='Markdown')
        await update.message.reply_text(texto_servicios, parse_mode='Markdown')

# ------ Button -----------------

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    pattern = r"\d{4}-\d{2}-\d{2}:\d{2}"
    query = update.callback_query

    await query.answer()
    if query.data == 'reservar':
        await reservas(update, context)
    elif query.data == 'horario':
        await query.edit_message_text(text="Nuestro horario es de lunes a viernes de 9:00 a 18:00.")
    elif query.data == 'contacto':
        await query.edit_message_text(text="Puedes enviarme un correo directo a lit.io30303@gmail.com")
    elif query.data == 'masinformacion':
        await servicios_mapping(update, context)





# ---------- AYUDA SECTION ---------
async def help(update: Update, context: ContextTypes):

    await update.message.reply_text("Para abrir el menu de opciones presiona /start")


# ---- Horarios --------
async def horarios(update: Update, context: ContextTypes):
    await update.message.reply_text("Nuestro horario es de lunes a viernes de 9:00 a 18:00.")


# ----- Eventos Proximos ------
async def upcoming_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        events = calendar_manager.list_upcoming_events()
        if events:
            events_text = "\n".join(events)
            await update.message.reply_text(f"Eventos próximos:\n{events_text}")
        else:
            await update.message.reply_text("No hay eventos próximos desde la fecha de hoy.")
    except Exception as e:
        await update.message.reply_text(f"Error al obtener los eventos: {e}")
        


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_data = context.user_data


    print(f"User Data: {user_data}")  # Debugging line to print user data



    if 'awaiting_start_time' in user_data and user_data['awaiting_start_time']:
        try:
            start_time = datetime.fromisoformat(text)
            user_data['start_time'] = start_time
            user_data['awaiting_start_time'] = False
            user_data['awaiting_end_time'] = True

            print(f"Start Time: {start_time}")  # Debugging line
            print(f"User Data after start time: {user_data}")  # Debugging line

            await update.message.reply_text("Por favor, envíame la fecha y hora de fin de la reserva en el formato AAAA-MM-DD HH:MM")

        except ValueError:
            await update.message.reply_text("Formato de fecha y hora inválido. Por favor, usa el formato AAAA-MM-DD HH:MM.")
        except Exception as e:
            await update.message.reply_text(f"Error al procesar la fecha y hora de inicio: {e}")

    elif 'awaiting_end_time' in user_data and user_data['awaiting_end_time']:
        try:
            end_time = datetime.fromisoformat(text)
            user_data['end_time'] = end_time
            user_data['awaiting_end_time'] = False
            user_data['awaiting_title'] = True

            print(f"End Time: {end_time}")  # Debugging line
            print(f"User Data after end time: {user_data}")  # Debugging line

            await update.message.reply_text("Por favor, envíame el título de la reserva.")

        except ValueError:
            await update.message.reply_text("Formato de fecha y hora inválido. Por favor, usa el formato AAAA-MM-DD HH:MM.")

        except Exception as e:
            await update.message.reply_text(f"Error al procesar la fecha y hora de fin: {e}")

    elif 'awaiting_title' in user_data and user_data['awaiting_title']:
        try:
            title = text
            start_time = user_data['start_time']
            end_time = user_data['end_time']

            print(f"Title: {title}")  # Debugging line
            print(f"Start Time: {start_time}, End Time: {end_time}")  # Debugging line

            if calendar_manager.is_time_slot_available(start_time, end_time):

                calendar_manager.create_event(title, start_time.isoformat(), end_time.isoformat(), 'America/Santiago')

                await update.message.reply_text("Reserva creada exitosamente.")
                
            else:
                await update.message.reply_text("La fecha y hora seleccionadas ya están ocupadas. Por favor, elige otro horario.")

            user_data.clear()

        except KeyError as e:
            await update.message.reply_text(f"Error al crear la reserva: falta {e}")
        except Exception as e:
            await update.message.reply_text(f"Error al crear la reserva: {e}")
    
    else:
        await update.message.reply_text("Para más información escribe /help")



# ----- ERROR ----
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.error)
    if update and update.message:
        await update.message.reply_text('Ha ocurrido un error')
    elif update and update.callback_query:
        await update.callback_query.message.reply_text('Ha ocurrido un error')


def run_bot() -> None:
    print('========= Iniciando Bot ==============')
    telegram_app = Application.builder().token(token).build()

    # Crear comandos
    telegram_app.add_handler(CommandHandler('start', start))
    telegram_app.add_handler(CommandHandler('reservas', reservas))
    telegram_app.add_handler(CommandHandler('upcoming', upcoming_events))
    telegram_app.add_handler(CommandHandler('servicios_mapping', servicios_mapping))

    telegram_app.add_handler(CallbackQueryHandler(button))

    telegram_app.add_handler(CommandHandler('help', help))
    telegram_app.add_handler(CommandHandler('horarios', horarios))

    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))




    # Crear errores
    telegram_app.add_error_handler(error)

    # Iniciar bot
    print('Bot iniciado')

    # Crear un nuevo bucle de eventos para el hilo del bot
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    telegram_app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
