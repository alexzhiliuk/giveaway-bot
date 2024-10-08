from datetime import datetime as dt
import time
from database import Database
from config import DB_NAME
from random import sample
from telebot.apihelper import ApiTelegramException

from bot import bot
from logger import bot_logger

from utils.get_admins import get_admins
from utils.create_admin_message import create_admin_message
from utils.giveaways_view import update_giveaway_status


def get_giveaway_participants(giveaway_id: int):
    with Database(DB_NAME) as db:
        return [participant[0] for participant in db.select(
            "SELECT user_id FROM giveaway_participants WHERE giveaway_id = ?",
            (giveaway_id, )
        )]


def set_giveaway_winners(giveaway_id: int, winners_id: tuple):
    with Database(DB_NAME) as db:

        db.update(
            f"UPDATE giveaway_participants SET is_winner = 1 WHERE user_id IN ({', '.join(list('?'*len(winners_id)))})",
            winners_id
        )
        bot_logger.info(
            f"Пользователи {winners_id} победили в розыгрыше {giveaway_id}")


def finish_giveaway(
        giveaway_id: int,
        giveaway_name: str,
        winners_count: int,
        message_for_winner: str,
        message_for_others: str):

    admins = get_admins()
    participants = get_giveaway_participants(giveaway_id)

    if len(participants) < winners_count:
        update_giveaway_status(giveaway_id, "FINISHED")
        for admin_id in admins:
            try:
                bot.send_message(
                    admin_id, f"Розыгрыш {giveaway_name} закончен, но участников было недостаточно", parse_mode="HTML")
            except ApiTelegramException:
                bot_logger.info(
                    f"Не удалось отправить сообщение админу {admin_id} о розыгрыше {giveaway_id}")
        return

    winners = sample(participants, winners_count)
    set_giveaway_winners(giveaway_id, tuple(winners))

    update_giveaway_status(giveaway_id, "FINISHED")

    for winner_id in winners:
        try:
            bot.send_message(winner_id, message_for_winner, parse_mode="HTML")
        except ApiTelegramException:
            bot_logger.info(
                f"Не удалось отправить сообщение победителю {winner_id} в розыгрыше {giveaway_id}")

    for another_participant_id in set(participants) - set(winners):
        try:
            bot.send_message(another_participant_id, message_for_others, parse_mode="HTML")
        except ApiTelegramException:
            bot_logger.info(
                f"Не удалось отправить сообщение участнику {another_participant_id} в розыгрыше {giveaway_id}")

    message_for_admin = create_admin_message(giveaway_name, giveaway_id)
    for admin_id in admins:
        try:
            bot.send_message(admin_id, message_for_admin, parse_mode="HTML")
        except ApiTelegramException:
            bot_logger.info(
                f"Не удалось отправить сообщение админу {admin_id} о розыгрыше {giveaway_id}")

    bot_logger.info(
        f"Розыгрыш {giveaway_id} завершен")


def check_giveaways_end_datetime():
    with Database(DB_NAME) as db:
        running_giveaways = db.select("SELECT "
                                      "id, end_datetime, name, winners_count, message_for_winner, message_for_others "
                                      "FROM giveaway WHERE status = 'RUN'")

        for running_giveaway in running_giveaways:
            end_datetime = dt.strptime(running_giveaway[1], "%Y-%m-%d %H:%M:%S")

            if dt.now() > end_datetime:
                finish_giveaway(running_giveaway[0], running_giveaway[2], running_giveaway[3], running_giveaway[4], running_giveaway[5])


