import re
from datetime import timedelta, datetime as dt
import logging
from threading import Timer
from config import *

import telebot
from utils import admin_registration, is_user_admin, register_participant
from keyboards.admin import kb_admin_menu
from exceptions.join_to_giveaway import *
from logger import bot_logger
from bot import bot


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):

    if len(message.text.split()) > 1:
        parameter = message.text.split()[-1]

        if parameter == ADMIN_PASS:

            admin_registration(message)

            bot.send_message(message.from_user.id, ADMIN_START_MESSAGE, reply_markup=kb_admin_menu)
            return

        if "join_to" in parameter:
            giveaway_id = int(parameter.split("_")[-1])

            try:
                register_participant(giveaway_id, message)
            except AdminParticipantError:
                bot_logger.info(f"Админ {message.from_user.id} попытался зарегистрироватсья в розыгрыше {giveaway_id}")
                bot.send_message(message.from_user.id, "Администратор не может участвовать в конкурсе")
                return
            except RepeatedRegistrationError:
                bot_logger.info(f"Пользователь {message.from_user.id} попытался зарегистрироватсья в розыгрыше повторно {giveaway_id}")
                bot.send_message(message.from_user.id, "Вы уже зарегистрированы в данном розыгрыше")
                return

            bot.send_message(message.from_user.id, "Вы зарегистрированы в конкурсе!")
            return

    else:
        if is_user_admin(message):
            bot.send_message(message.chat.id, ADMIN_START_MESSAGE, reply_markup=kb_admin_menu)
            return

        bot.send_message(message.chat.id, USER_START_MESSAGE)


@bot.message_handler(commands=['menu'])
def menu(message: telebot.types.Message):

    if not is_user_admin(message):
        return

    bot.send_message(message.chat.id, "Стартовое сообщение для админа", reply_markup=kb_admin_menu)


from handlers.admin import *
from utils.finish_giveaway import *


def my_task():
    check_giveaways_end_datetime()
    return False


def set_interval(timer, task):
    is_stop = task()
    if not is_stop:
        Timer(timer, set_interval, [timer, task]).start()


if __name__ == "__main__":

    set_interval(30, my_task)

    bot.polling(none_stop=True)
