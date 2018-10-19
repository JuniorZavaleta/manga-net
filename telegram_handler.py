# -*- coding: utf-8 -*-
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, ConversationHandler,
                          CallbackQueryHandler, MessageHandler, Filters)
from datetime import datetime
import config

bot = telegram.Bot(token=config.TELEGRAM_TOKEN)
updater = Updater(config.TELEGRAM_TOKEN)


# Utils
def build_menu(buttons, n_cols):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    return menu


# Commands
def start(bot, update):
    # Check if messenger's chat id already exists
    chat_id = update.message.chat.id
    _from = update.message.from_user

    message = u'Hola {}'.format(_from.first_name)

    update.message.reply_text(message)


def add_image(bot, update):
    chat_id = update.message.chat.id
    file_id = update.message.photo[-1].file_id
    photo_file = bot.get_file(file_id)
    file_path = 'static/telegram_images/{}.jpg'.format(file_id)
    photo_file.download(file_path)


def cancel(bot, update):
    update.message.reply_text("Entiendo, nos vemos luego.")

    return ConversationHandler.END


def ask_new_prediction(bot, update):
    keyboard = [[InlineKeyboardButton('Si :)', callback_data='wait_for_image'),
                 InlineKeyboardButton('NO :(', callback_data='nothing')]]

    update.message.reply_text(u'¿Deseas predecir una imagen de un manga?',
                              reply_markup=InlineKeyboardMarkup(keyboard))


def wait_for_image(bot, update):
    update.callback_query.message.reply_text(u'Ok, adjunte la imagen.')
    return LOAD_IMAGE


def predict_image(bot, update):
    add_image(bot, update)
    # TODO: Poner predicción aquí
    update.message.reply_text(u"La predicción aún no está habilitada")

    keyboard = [[InlineKeyboardButton('Si', callback_data='wait_for_image'),
                 InlineKeyboardButton('No', callback_data='ok_thanks')]]
    update.message.reply_text(u'¿Deseas agregar otra imagen?',
                              reply_markup=InlineKeyboardMarkup(keyboard))

    return OK_THANKS


def ok_thanks(bot, update):
    update.callback_query.message.reply_text(u'Ok, nos vemos.')


(LOAD_IMAGE, OK_THANKS) = range(2)

# Handlers
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('new', ask_new_prediction))
updater.dispatcher.add_handler(ConversationHandler(
    entry_points=[CallbackQueryHandler(wait_for_image, pattern='wait_for_image')],
    states={
        LOAD_IMAGE: [MessageHandler(Filters.photo, predict_image)],
        OK_THANKS: [CallbackQueryHandler(ok_thanks, pattern='ok_thanks')]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
))
