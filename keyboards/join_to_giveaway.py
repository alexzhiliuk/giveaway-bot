from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def kb_join(giveaway_id: int, bot_username: str):
    kb = InlineKeyboardMarkup()

    kb.add(InlineKeyboardButton(f"Участвую!", url=f"https://t.me/{bot_username}?start=join_to_{giveaway_id}"))

    return kb
