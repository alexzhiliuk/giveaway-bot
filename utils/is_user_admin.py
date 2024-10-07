from config import DB_NAME
from database import Database
from telebot.types import Message

from utils.user_registration import user_registration


def is_user_admin(message: Message):
    with Database(DB_NAME) as db:
        try:
            user_status: tuple[str] = db.select("SELECT status FROM users WHERE id = ?", (message.from_user.id, ))[0]
        except IndexError:
            user_registration(message)
            return False
        else:
            return user_status[0] == "ADMIN"

