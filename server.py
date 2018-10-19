import telegram
from flask import Flask, request

from telegram_handler import bot, updater
import config

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/set', methods=['GET', 'POST'])
def set_webhook():
    if bot.setWebhook(config.SITE_URL + 'telegram'):
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/telegram', methods=['POST'])
def handle_telegram_request():
    if request.method == "POST":
        # retrieve the message in JSON and then transform it to Telegram object
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        updater.dispatcher.process_update(update)

    return 'ok'
