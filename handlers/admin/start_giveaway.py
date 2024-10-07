import re
from datetime import time, datetime as dt
import telebot

from bot import bot
from config import ADMIN_START_MESSAGE
from keyboards import kb_admin_menu

from keyboards.admin.calendar import DialogCalendar
from utils.creating_giveaways import *


@bot.callback_query_handler(func=lambda data: re.fullmatch(r"start_giveaway", data.data))
def start_giveaway(data: telebot.types.CallbackQuery):
    delete_unfilled_giveaways(data.from_user.id)

    user_giveaways = get_user_creating_giveaways(data.from_user.id)
    if user_giveaways:
        user_giveaways = " ".join([giveaway[0] for giveaway in user_giveaways])
        bot.send_message(
            data.from_user.id, f"У вас есть недосозданные розыгрыши ({user_giveaways}), удалите их, чтобы создать новый"
        )
        return

    send = bot.send_message(
        data.from_user.id, "Введите название нового розыгрыша"
    )
    bot.register_next_step_handler(send, input_giveaway_name)


def input_giveaway_name(message: telebot.types.Message):
    if message.content_type != "text":
        send = bot.send_message(message.from_user.id, "Введите название нового розыгрыша (только текст)")
        bot.register_next_step_handler(send, input_giveaway_name)
        return

    send = bot.send_message(message.from_user.id, "Введите текст для розыгрыша")
    bot.register_next_step_handler(send, input_giveaway_text, {"name": message.text, "owner": message.from_user.id})


def input_giveaway_text(message: telebot.types.Message, giveaway_info: dict):
    if message.content_type != "text":
        send = bot.send_message(message.from_user.id, "Введите текст нового розыгрыша (только текст)")
        bot.register_next_step_handler(send, input_giveaway_text, giveaway_info)
        return

    giveaway_info["text"] = message.text
    send = bot.send_message(message.from_user.id, "Введите количество победителей")
    bot.register_next_step_handler(send, input_giveaway_winners_count, giveaway_info)


def input_giveaway_winners_count(message: telebot.types.Message, giveaway_info: dict):
    if message.content_type != "text" or not message.text.isnumeric():
        send = bot.send_message(message.from_user.id, "Введите количество победителей")
        bot.register_next_step_handler(send, input_giveaway_winners_count, giveaway_info)
        return

    giveaway_info["winners_count"] = int(message.text)
    send = bot.send_message(message.from_user.id, "Введите сообщение для победителя")
    bot.register_next_step_handler(send, input_giveaway_message_for_winner, giveaway_info)


def input_giveaway_message_for_winner(message: telebot.types.Message, giveaway_info: dict):
    if message.content_type != "text":
        send = bot.send_message(message.from_user.id, "Введите сообщение для победителя (только текст)")
        bot.register_next_step_handler(send, input_giveaway_message_for_winner, giveaway_info)
        return

    giveaway_info["message_for_winner"] = message.text
    send = bot.send_message(message.from_user.id, "Введите сообщение для остальных участников")
    bot.register_next_step_handler(send, input_giveaway_message_for_others, giveaway_info)


def input_giveaway_message_for_others(message: telebot.types.Message, giveaway_info: dict):
    if message.content_type != "text":
        send = bot.send_message(message.from_user.id, "Введите сообщение для остальных участников (только текст)")
        bot.register_next_step_handler(send, input_giveaway_message_for_others, giveaway_info)
        return

    giveaway_info["message_for_others"] = message.text
    create_giveaway(giveaway_info)

    bot.send_message(message.from_user.id, "Выберите дату и время окончания розыгрыша", reply_markup=DialogCalendar.start_calendar(dt.now().year))


@bot.callback_query_handler(func=lambda data: re.fullmatch(r"START-YEAR", data.data))
def start_year(data: telebot.types.CallbackQuery):
    bot.edit_message_text("Выберите дату и время окончания розыгрыша", data.from_user.id, data.message.id, reply_markup=DialogCalendar.start_calendar(dt.now().year))


@bot.callback_query_handler(func=lambda data: re.fullmatch(r"START-MONTH \d+", data.data))
@bot.callback_query_handler(func=lambda data: re.fullmatch(r"SET-YEAR \d+", data.data))
def set_year(data: telebot.types.CallbackQuery):
    year = int(data.data.split()[-1])
    bot.edit_message_text("Выберите дату и время окончания розыгрыша", data.from_user.id, data.message.id, reply_markup=DialogCalendar.get_month_kb(year))


@bot.callback_query_handler(func=lambda data: re.fullmatch(r"SET-MONTH \d+ \d+", data.data))
def set_month(data: telebot.types.CallbackQuery):
    year, month = int(data.data.split()[-2]), int(data.data.split()[-1])
    bot.edit_message_text("Выберите дату и время окончания розыгрыша", data.from_user.id, data.message.id, reply_markup=DialogCalendar.get_days_kb(year, month))


@bot.callback_query_handler(func=lambda data: re.fullmatch(r"SET-DAY \d+ \d+ \d+", data.data))
def set_day(data: telebot.types.CallbackQuery):
    year, month, day = map(int, data.data.split()[1:])
    bot.edit_message_text(
        f"Дата окончания розыгрыша {dt(year, month, day).strftime('%Y-%m-%d')}",
        data.from_user.id, data.message.id,
        reply_markup=DialogCalendar.get_confirm_kb(year, month, day)
    )


@bot.callback_query_handler(func=lambda data: re.fullmatch(r"SET-DATE \d+ \d+ \d+", data.data))
def set_date(data: telebot.types.CallbackQuery):
    year, month, day = map(int, data.data.split()[1:])
    update_giveaway_datetime(dt(year, month, day), data.from_user.id)

    bot.edit_message_text(
        f"Введите время для окончания розыгрыша",
        data.from_user.id, data.message.id
    )
    send = bot.send_message(data.from_user.id, "Например: 19:00")
    bot.register_next_step_handler(send, input_giveaway_end_time)


def input_giveaway_end_time(message: telebot.types.Message):
    if message.content_type != "text" or not re.fullmatch(r"\d\d:\d\d", message.text.strip()):
        send = bot.send_message(message.from_user.id, "Введите время для окончания розыгрыша\nНапример: 19:00")
        bot.register_next_step_handler(send, input_giveaway_end_time)
        return

    hour, minute = map(int, message.text.split(":"))
    update_giveaway_end_time(time(hour, minute), message.from_user.id)
    giveaway_summary = get_giveaway_creating_summary(message.from_user.id)

    answer = f"""{giveaway_summary['text']}

<b>Дата окончания:</b> {giveaway_summary['end_datetime']}

<b>Количество победителей:</b> {giveaway_summary['winners_count']}

<b>Сообщение для победителей:</b>
{giveaway_summary['message_for_winner']}

<b>Сообщение для остальных участников:</b>
{giveaway_summary['message_for_others']}
"""

    finish_creating_giveaway(message.from_user.id)
    bot.send_message(message.from_user.id, answer, parse_mode="HTML")

    bot.send_message(message.chat.id, ADMIN_START_MESSAGE, reply_markup=kb_admin_menu)
