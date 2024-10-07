from flask import Flask, request

import telebot
from bot import bot, TOKEN


app = Flask(__name__)

PROJECT_NAME = "zhiliuk.pythonanywhere.com"


@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f'https://{PROJECT_NAME}/' + TOKEN)
    return "!", 200
