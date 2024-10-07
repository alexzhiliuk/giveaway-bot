from database import Database
from config import DB_NAME
from utils import get_giveaway_winners


def create_admin_message(giveaway_name: str, giveaway_id: int) -> str:
    message: str = f"Победители конкурса <b>{giveaway_name}</b>\n"

    with Database(DB_NAME) as db:
        winners = get_giveaway_winners(giveaway_id)

        for winner in winners:
            message += f"\n@{winner[1]} {winner[2]} {winner[3]}"

    return message
