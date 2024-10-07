from config import DB_NAME
from database import Database
from telebot.types import Message

from logger import bot_logger


def user_registration(message: Message):
    with Database(DB_NAME) as db:
        try:
            user = db.select("SELECT * FROM users WHERE id = ?", (message.from_user.id,))[0]
        except IndexError:
            db.insert("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (
                message.from_user.id,
                message.from_user.username,
                message.from_user.first_name,
                message.from_user.last_name,
                "USER"
            ))
            bot_logger.info(
                f"Пользователь {message.from_user.id} {message.from_user.username} зарегистрирован")
