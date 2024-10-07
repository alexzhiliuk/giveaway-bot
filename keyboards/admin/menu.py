from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

btn_giveaways = InlineKeyboardButton("Розыгрыши", callback_data="giveaways")
btn_start_giveaway = InlineKeyboardButton("Начать новый розыгрыш", callback_data="start_giveaway")

kb_admin_menu = InlineKeyboardMarkup().add(btn_giveaways).add(btn_start_giveaway)
