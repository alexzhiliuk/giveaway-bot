from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.giveaways_view import get_giveaways_for_kb


statuses = {
    "CREATING": "Создается",
    "PENDING": "Создан",
    "RUN": "Запущен",
    "FINISHED": "Закончен",
}


def kb_all_giveaways():
    kb_giveaways = InlineKeyboardMarkup()

    for giveaway_id, giveaway_name, status in get_giveaways_for_kb():
        kb_giveaways.add(InlineKeyboardButton(f"{giveaway_name} - {statuses[status]}", callback_data=f"giveaway_view_{giveaway_id}"))

    return kb_giveaways


def kb_giveaway(status, giveaway_id):
    kb_giveaway_markup = InlineKeyboardMarkup()

    if status == "PENDING":
        kb_giveaway_markup.add(InlineKeyboardButton(f"Запустить", callback_data=f"giveaway_run_{giveaway_id}"))

    kb_giveaway_markup.add(InlineKeyboardButton(f"---Удалить---", callback_data=f"giveaway_delete_{giveaway_id}"))
    kb_giveaway_markup.add(InlineKeyboardButton(f"<<< Назад", callback_data=f"giveaways"))

    return kb_giveaway_markup


def kb_confirm_delete_giveaway(giveaway_id):
    kb_giveaway_markup = InlineKeyboardMarkup()

    kb_giveaway_markup.add(InlineKeyboardButton(f"Удалить", callback_data=f"giveaway_confirm_delete_{giveaway_id}"))
    kb_giveaway_markup.add(InlineKeyboardButton(f"<<< Назад", callback_data=f"giveaway_view_{giveaway_id}"))

    return kb_giveaway_markup
