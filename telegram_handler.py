# -*- coding: utf-8 -*-
import torch
import numpy as np

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, ConversationHandler,
                          CallbackQueryHandler, MessageHandler, Filters)

import config
from cnn import MangaNet
from preprocessing import preprocesamiento_telegram
from skimage import io

bot = telegram.Bot(token=config.TELEGRAM_TOKEN)
updater = Updater(config.TELEGRAM_TOKEN)

model = MangaNet(8)
checkpoint = torch.load('model.ckpt')
classes = ['Peleas', 'Fantasia', '4 paneles', 'Drama Histórico', 'Terror', 'Humor', 'Romance',
           'Comedia romántica', 'Ciencia ficción', 'Deportes', 'Suspenso']


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

    return file_id


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
    file_id = add_image(bot, update)
    images = preprocesamiento_telegram(str(file_id))

    model.load_state_dict(checkpoint)

    predicted_set = set()
    for image_path in images:
        image = io.imread(image_path, as_gray=True)
        image = image[:, :, np.newaxis]
        image = image.transpose((2, 0, 1))
        image = torch.from_numpy(image)
        image = image.type('torch.FloatTensor')
        outputs = model(image.unsqueeze(0))
        predicted_t = torch.sigmoid(outputs).data > 0.2
        _predicted = predicted_t.numpy().flatten()
        predicted = np.argwhere(_predicted == 1).flatten()
        for i in predicted:
            print(classes[i])
            predicted_set.add(classes[i])

    update.message.reply_text(u"Etiquetas: {}".format(', '.join(predicted_set)))

    keyboard = [[InlineKeyboardButton('Si', callback_data='wait_for_image'),
                 InlineKeyboardButton('No', callback_data='ok_thanks')]]
    update.message.reply_text(u'¿Deseas agregar otra imagen?',
                              reply_markup=InlineKeyboardMarkup(keyboard))

    return OK_THANKS


def ok_thanks(bot, update):
    update.callback_query.message.reply_text(u'Ok, nos vemos.')

    return ConversationHandler.END


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
