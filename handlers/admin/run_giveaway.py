import re
import telebot

from bot import bot
from config import CHANNEL_ID

from keyboards.admin.giveaways import kb_all_giveaways
from keyboards.join_to_giveaway import kb_join
from utils.giveaways_view import update_giveaway_status, get_giveaway_text


@bot.callback_query_handler(func=lambda data: re.fullmatch(r"giveaway_run_\d+", data.data))
def giveaway_run(data: telebot.types.CallbackQuery):
    giveaway_id = int(data.data.split("_")[-1])

    update_giveaway_status(giveaway_id, "RUN")

    bot.send_message(CHANNEL_ID, get_giveaway_text(giveaway_id), reply_markup=kb_join(giveaway_id, bot.get_me().username))

    bot.edit_message_text(
        "Розыгрыши:", data.from_user.id, data.message.id, reply_markup=kb_all_giveaways()
    )
