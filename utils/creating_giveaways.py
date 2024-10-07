from datetime import datetime as dt

from config import DB_NAME
from database import Database
from logger import bot_logger


def get_user_creating_giveaways(owner: int | str) -> list:
    with Database(DB_NAME) as db:
        return db.select("SELECT name FROM giveaway WHERE owner = ? AND status = 'CREATING'",(owner, ))


def create_giveaway(giveaway_info: dict):
    values = (
        giveaway_info["name"],
        giveaway_info["owner"],
        giveaway_info["text"],
        giveaway_info["winners_count"],
        giveaway_info["message_for_winner"],
        giveaway_info["message_for_others"],
    )

    with Database(DB_NAME) as db:
        db.insert("INSERT INTO giveaway (name, owner, text, winners_count, message_for_winner, message_for_others) "
                  "VALUES (?, ?, ?, ?, ?, ?)", values)


def delete_unfilled_giveaways(owner: int | str):
    with Database(DB_NAME) as db:
        db.delete("DELETE FROM giveaway WHERE end_datetime IS NULL AND owner = ?", (owner,))
        bot_logger.info(
            f"Удалены все незаполненные розыгрыши пользователя {owner}")


def update_giveaway_datetime(end_datetime, owner: int | str):
    with Database(DB_NAME) as db:
        db.update(
            "UPDATE giveaway SET end_datetime = ? WHERE owner = ? AND status = 'CREATING'",
            (end_datetime, owner)
        )


def update_giveaway_end_time(end_time, owner: int | str):
    with Database(DB_NAME) as db:
        giveaway_end_datetime = db.select(
            "SELECT end_datetime FROM giveaway WHERE owner = ? AND status = 'CREATING'",
            (owner, ))[0]

        giveaway_end_datetime = dt.strptime(giveaway_end_datetime[0], "%Y-%m-%d %H:%M:%S")
        giveaway_end_datetime = dt.combine(giveaway_end_datetime, end_time)
        db.update(
            "UPDATE giveaway SET end_datetime = ? WHERE owner = ? AND status = 'CREATING'",
            (giveaway_end_datetime, owner)
        )


def finish_creating_giveaway(owner: int | str):
    with Database(DB_NAME) as db:
        db.update(
            "UPDATE giveaway SET status = 'PENDING' WHERE owner = ? AND status = 'CREATING'",
            (owner, )
        )
        bot_logger.info(
            f"Пользователь {owner} создал новый розыгрыш")


def get_giveaway_creating_summary(owner: int | str):
    with Database(DB_NAME) as db:
        giveaway_summary = db.select(
            "SELECT text, winners_count, message_for_winner, message_for_others, end_datetime FROM giveaway WHERE owner = ? AND status = 'CREATING'",
            (owner, )
        )[0]
        return {
            "text": giveaway_summary[0],
            "winners_count": giveaway_summary[1],
            "message_for_winner": giveaway_summary[2],
            "message_for_others": giveaway_summary[3],
            "end_datetime": giveaway_summary[4],
        }


