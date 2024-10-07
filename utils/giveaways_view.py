from database import Database
from config import DB_NAME
from logger import bot_logger


def get_giveaways_for_kb():

    with Database(DB_NAME) as db:

        return db.select("SELECT id, name, status FROM giveaway")


def get_giveaway_summary(giveaway_id: int):
    with Database(DB_NAME) as db:
        giveaway_summary = db.select(
            "SELECT id, text, winners_count, message_for_winner, message_for_others, end_datetime, status FROM giveaway WHERE id = ?",
            (giveaway_id, )
        )[0]
        return {
            "id": giveaway_summary[0],
            "text": giveaway_summary[1],
            "winners_count": giveaway_summary[2],
            "message_for_winner": giveaway_summary[3],
            "message_for_others": giveaway_summary[4],
            "end_datetime": giveaway_summary[5],
            "status": giveaway_summary[6],
        }


def get_giveaway_winners(giveaway_id: int):
    with Database(DB_NAME) as db:
        return db.select(
            "SELECT u.id, u.username, u.first_name, u.last_name "
            "FROM giveaway_participants gw "
            "JOIN users u ON u.id = gw.user_id "
            "WHERE giveaway_id = ? AND is_winner = 1",
            (giveaway_id,)
        )


def delete_giveaway(giveaway_id: int):
    with Database(DB_NAME) as db:
        db.delete("DELETE FROM giveaway WHERE id = ?", (giveaway_id,))
        bot_logger.info(
            f"Розыгрыш {giveaway_id} был удален")


def update_giveaway_status(giveaway_id: int, status: str):
    with Database(DB_NAME) as db:
        db.update("UPDATE giveaway SET status = ? WHERE id = ?", (status, giveaway_id))
        bot_logger.info(
            f"Статус розыгрыша {giveaway_id} обновлен на {status}")


def get_giveaway_text(giveaway_id: int):
    with Database(DB_NAME) as db:
        return db.select(
            "SELECT text FROM giveaway WHERE id = ?",
            (giveaway_id, )
        )[0]


