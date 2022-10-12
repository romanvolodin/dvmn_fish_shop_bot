from environs import Env
import redis
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Filters, Updater
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler

from store import get_access_token, fetch_products

_database = None

def start(update, context):
    db = context.bot_data['db']
    access_token = db.get('access_token').decode('utf-8')
    products = fetch_products(access_token)
    keyboard = [
        [InlineKeyboardButton(product['name'], callback_data=product['id'])]
        for product in products
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    return 'ECHO'


def echo(update, context):
    query = update.callback_query
    users_reply = update.message.text
    update.message.reply_text(query)
    return 'ECHO'


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

    client_id = env.str('EP_CLIENT_ID')
    client_secret = env.str('EP_CLIENT_SECRET')
    telegram_token = env.str('TELEGRAM_TOKEN')
    database_password = env.str('DATABASE_PASSWORD')
    database_host = env.str('DATABASE_HOST')
    database_port = env.int('DATABASE_PORT')
    db = redis.Redis(
        host=database_host,
        port=database_port,
        password=database_password
    )
    access_token = get_access_token(client_id, client_secret)
    
    db.set('access_token', access_token)

    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data['db'] = db
    dispatcher.add_handler(CallbackQueryHandler(handle_users_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_users_reply))
    dispatcher.add_handler(CommandHandler('start', handle_users_reply))
    updater.start_polling()
