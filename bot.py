import redis
from environs import Env
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater)

from store import (download_product_image, fetch_product, fetch_product_price,
                   fetch_product_stock, fetch_products, get_access_token)


def start(update, context):
    db = context.bot_data['db']
    access_token = db.get('access_token').decode('utf-8')
    products = fetch_products(access_token)
    keyboard = [
        [InlineKeyboardButton(product['attributes']['name'], callback_data=product['id'])]
        for product in products
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    return 'HANDLE_MENU'


def handle_menu(update, context):
    db = context.bot_data['db']
    token = db.get('access_token').decode("utf-8")
    price_book_id = db.get('price_book_id').decode("utf-8")
    context.bot.delete_message(
        chat_id=update.effective_chat.id,
        message_id=update.callback_query.message.message_id,
    )
    callback = update.callback_query.data
    product_id = callback
    product = fetch_product(product_id, token)
    product_price = fetch_product_price(price_book_id, product['attributes']['sku'], token)
    product_stock = fetch_product_stock(product_id, token)
    product_image = download_product_image(
        product['relationships']['main_image']['data']['id'], access_token
    )
    name = product['attributes']['name']
    price = product_price['attributes']['currencies']['USD']['amount']
    formated_price = "${:.2f}".format(price / 100)
    stock = product_stock['available']
    description = product['attributes']['description']
    text = f'{name}\n\n{formated_price} per kg\n{stock} kg on stock\n\n{description}'

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="go_back")]])

    with open(product_image, 'rb') as photo:
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption=text,
            reply_markup=reply_markup,
        )
    return 'HANDLE_DESCRIPTION'


def handle_description(update, context):
    db = context.bot_data['db']
    token = db.get('access_token').decode("utf-8")
    callback = update.callback_query.data
    if callback == 'go_back':
        context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=update.callback_query.message.message_id,
        )
        products = fetch_products(token)
        keyboard = [
            [InlineKeyboardButton(product['attributes']['name'], callback_data=product['id'])]
            for product in products
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Выберите товар:',
            reply_markup=reply_markup
        )
        return 'HANDLE_MENU'


def handle_users_reply(update, context):
    db = context.bot_data['db']
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
        user_state = db.get(chat_id).decode("utf-8")
    
    states_functions = {
        'START': start,
        'HANDLE_MENU': handle_menu,
        'HANDLE_DESCRIPTION': handle_description,
    }
    state_handler = states_functions[user_state]
    try:
        next_state = state_handler(update, context)
        db.set(chat_id, next_state)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    env = Env()
    env.read_env()

    client_id = env.str('EP_CLIENT_ID')
    client_secret = env.str('EP_CLIENT_SECRET')
    price_book_id = env.str('EP_PRICEBOOK_ID')
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
    db.set('price_book_id', price_book_id)

    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data['db'] = db
    dispatcher.add_handler(CallbackQueryHandler(handle_users_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_users_reply))
    dispatcher.add_handler(CommandHandler('start', handle_users_reply))
    updater.start_polling()
