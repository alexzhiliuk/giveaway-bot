import os
from flask import Flask, request

import telebot
from bot import bot
from config import TOKEN

from threading import Timer
from utils.finish_giveaway import check_giveaways_end_datetime


app = Flask(__name__)

BASE_URL = os.environ.get('BASE_URL', 80)


@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f'{BASE_URL}/' + TOKEN)
    return "!", 200


from main import start, menu


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


if __name__ == "__main__":
    set_interval(30, my_task)

    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 80)))
