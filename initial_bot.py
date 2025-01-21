from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters,ContextTypes
import os
from dotenv import load_dotenv


load_dotenv()

token = os.getenv("TOKEN_API")
user_name = os.getenv("USER_BOT")


"""
Para setear los comandos aplicar esto en BotFather
/setcommands

"""

# Comandos
async def start(update: Update, context: ContextTypes):
    await update.message.reply_text("Hola, soy un bot. ¿En que puedo ayudarte?")

async def help(update: Update, context: ContextTypes):
    await update.message.reply_text("Ayuda")

async def custom(update: Update, context: ContextTypes):
    await update.message.reply_text(update.message.text)




def handle_response(text: str, context: ContextTypes, update:Update):
    proccesed_text = text.lower()
    print(proccesed_text)
    
    if 'hola' in proccesed_text:
        return 'Hola, ¿Como estas?'
    elif 'adios' in proccesed_text:
        return 'Adios'
    else:
        return 'No te entiendo'




async def handle_message(update: Update, context: ContextTypes):
    message_type = update.message.chat.type
    text = update.message.text

    if message_type == 'group':
        if text.startswith(user_name):
            new_text = text.replace(user_name, '')
            response = handle_response(new_text, context, update)
        else:
            return
    else:
        response = handle_response(text, context, update)
    
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes):
    print(context.error)
    await update.message.reply_text('Ha ocurrido un error')

if __name__ == '__main__':
    print('========= Iniciando Bot ==============')
    app = Application.builder().token(token).build()

    # Crear comandos
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(CommandHandler('custom', custom))


    # Crear respuestas

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Crear errores
    app.add_error_handler(error)

    # Iniciar bot
    print('Bot iniciado')
    app.run_polling(poll_interval=1, timeout=10)