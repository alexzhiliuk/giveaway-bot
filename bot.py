from config import TOKEN

import telebot
from logger import bot_logger


if not TOKEN:
    bot_logger.info("Нет токена")
    raise Exception("Нет токена")

bot = telebot.TeleBot(TOKEN)
