from flask import Flask, request

import telebot
from bot import bot
from config import TOKEN

from threading import Timer
from utils.finish_giveaway import check_giveaways_end_datetime


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


def my_task():
    check_giveaways_end_datetime()
    return False


def set_interval(timer, task):
    is_stop = task()
    try:
        if not is_stop:
            Timer(timer, set_interval, [timer, task]).start()
        bot.send_message(625855750, "end interval")
    except:
        bot.send_message(625855750, "end interval error")


set_interval(30, my_task)
