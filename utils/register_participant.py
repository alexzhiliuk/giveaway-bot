from config import DB_NAME
from database import Database
from utils.is_user_admin import is_user_admin
from telebot.types import Message
from exceptions.join_to_giveaway import AdminParticipantError, RepeatedRegistrationError
from sqlite3 import IntegrityError
from logger import bot_logger


def register_participant(giveaway_id: int, message: Message):

    if is_user_admin(message):
        raise AdminParticipantError

    with Database(DB_NAME) as db:
        try:
            db.insert(
                "INSERT INTO giveaway_participants (user_id, giveaway_id) VALUES (?, ?)",
                (message.from_user.id, giveaway_id)
            )
            bot_logger.info(
                f"Пользователь {message.from_user.id} {message.from_user.username} зарегистрировался в розыгрыше {giveaway_id} ")
        except IntegrityError:
            raise RepeatedRegistrationError
        except:
            bot_logger.info(
                f"У пользователя {message.from_user.id} {message.from_user.username} произошла ошибка при регистрации в розыгрыше ")
