from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters,ContextTypes, CallbackQueryHandler, PreCheckoutQueryHandler
import os
from dotenv import load_dotenv

from reservas import GoogleCalendarManager
from datetime import datetime, timedelta

load_dotenv()

token = os.getenv("TOKEN_API_RESERVAS")
user_name = os.getenv("USER_BOT_RESERVAS")

URL_IG = "https://www.instagram.com/lllit_3/"
MAPS = "https://maps.app.goo.gl/JF7qNA8vXvBfKEu9A"

calendar_manager = GoogleCalendarManager()

"""
Para setear los comandos aplicar esto en BotFather
/setcommands

"""

# Comandos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    keyboard = [
        [
            InlineKeyboardButton("📖 Reservar cita", callback_data="reservar"),
            InlineKeyboardButton("🎨 Nuestros Servicios", url=URL_IG),
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


    await update.message.reply_text("🖖 Bienvenido, ¿Que te gustaria hacer?", reply_markup=reply_markup)


async def reservas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if update.message:
        await update.message.reply_text("Fecha de Inicio y Hora de Inicio\nFormato: AAAA-MM-DD HH:MM")
    elif update.callback_query:
        await update.callback_query.message.reply_text("Fecha de Inicio y Hora de Inicio\nFormato: AAAA-MM-DD HH:MM")
    context.user_data['awaiting_start_time'] = True
    print(f"User Data after /reservas: {context.user_data}")  # Debugging line

async def servicios_mapping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

    


    await update.message.reply_text(texto_servicios, parse_mode='Markdown')


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






async def help(update: Update, context: ContextTypes):
    await update.message.reply_text("Para abrir el menu de opciones presiona /start")

async def horarios(update: Update, context: ContextTypes):
    await update.message.reply_text("Nuestro horario es de lunes a viernes de 9:00 a 18:00.")


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




async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.error)
    if update.message:
        await update.message.reply_text('Ha ocurrido un error')
    elif update.callback_query:
        await update.callback_query.message.reply_text('Ha ocurrido un error')


def main() -> None:
    print('========= Iniciando Bot ==============')
    app = Application.builder().token(token).build()

    # Crear comandos
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('reservas', reservas))
    app.add_handler(CommandHandler('upcoming', upcoming_events))
    app.add_handler(CommandHandler('servicios_mapping', servicios_mapping))

    app.add_handler(CallbackQueryHandler(button))

    app.add_handler(CommandHandler('help', help))
    app.add_handler(CommandHandler('horarios', horarios))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))




    # Crear errores
    app.add_error_handler(error)

    # Iniciar bot
    print('Bot iniciado')
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()