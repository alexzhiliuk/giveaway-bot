import re
import telebot

from bot import bot

from keyboards.admin.giveaways import *
from utils.giveaways_view import get_giveaway_summary, get_giveaway_winners, delete_giveaway


@bot.callback_query_handler(func=lambda data: re.fullmatch(r"giveaways", data.data))
def giveaways_view(data: telebot.types.CallbackQuery):
    bot.edit_message_text(
        "Розыгрыши:", data.from_user.id, data.message.id, reply_markup=kb_all_giveaways()
    )


@bot.callback_query_handler(func=lambda data: re.fullmatch(r"giveaway_view_\d+", data.data))
def giveaway_view(data: telebot.types.CallbackQuery):
    giveaway_id = int(data.data.split("_")[-1])
    giveaway_summary = get_giveaway_summary(giveaway_id)

    answer = f"""<b>Статус</b>: {statuses[giveaway_summary['status']]}
    
{giveaway_summary['text']}

<b>Дата окончания:</b> {giveaway_summary['end_datetime']}

<b>Количество победителей:</b> {giveaway_summary['winners_count']}

<b>Сообщение для победителей:</b>
{giveaway_summary['message_for_winner']}

<b>Сообщение для остальных участников:</b>
{giveaway_summary['message_for_others']}
"""
    if giveaway_summary['status'] == "FINISHED":
        answer += "\n<b>Победители:</b>\n"
        winners = get_giveaway_winners(giveaway_id)
        for winner in winners:
            answer += f"\n@{winner[1]} {winner[2]} {winner[3]}\n"

    bot.edit_message_text(
        answer, data.from_user.id, data.message.id, parse_mode="HTML", reply_markup=kb_giveaway(
            giveaway_summary['status'],
            giveaway_summary['id']
        )
    )


@bot.callback_query_handler(func=lambda data: re.fullmatch(r"giveaway_delete_\d+", data.data))
def giveaway_delete(data: telebot.types.CallbackQuery):
    giveaway_id = int(data.data.split("_")[-1])

    bot.edit_message_text(
        "Удалить розыгрыш?",
        data.from_user.id, data.message.id,
        reply_markup=kb_confirm_delete_giveaway(giveaway_id)
    )


@bot.callback_query_handler(func=lambda data: re.fullmatch(r"giveaway_confirm_delete_\d+", data.data))
def giveaway_confirm_delete(data: telebot.types.CallbackQuery):
    giveaway_id = int(data.data.split("_")[-1])

    delete_giveaway(giveaway_id)

    bot.edit_message_text(
        "Розыгрыши:", data.from_user.id, data.message.id, reply_markup=kb_all_giveaways()
    )
