from environs import Env

from telegram.ext import Filters, Updater
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler

_database = None

def start(update, context):
    update.message.reply_text(text='Привет!')
    return "ECHO"


def echo(update, context):
    users_reply = update.message.text
    update.message.reply_text(users_reply)
    return "ECHO"


def handle_users_reply(update, context):
    db = get_database_connection()
    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id
    elif update.callback_query:
        user_reply = update.callback_query.data
        chat_id = update.callback_query.message.chat_id
    else:
        return
    if user_reply == '/start':
        user_state = 'START'
    else:
        user_state = db.get(chat_id)
    
    states_functions = {
        'START': start,
        'ECHO': echo
    }
    state_handler = states_functions[user_state]
    try:
        next_state = state_handler(update, context)
        db[chat_id] = next_state
    except Exception as err:
        print(err)

def get_database_connection():
    global _database
    if _database is None:
        _database = {}
    return _database


if __name__ == '__main__':
    env = Env()
    env.read_env()
    updater = Updater(env.str('TELEGRAM_TOKEN'))
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(handle_users_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_users_reply))
    dispatcher.add_handler(CommandHandler('start', handle_users_reply))
    updater.start_polling()
