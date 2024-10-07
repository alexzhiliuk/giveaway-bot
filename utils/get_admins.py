from database import Database
from config import DB_NAME


def get_admins():
    with Database(DB_NAME) as db:
        return [admin[0] for admin in db.select("SELECT id FROM users WHERE status = 'ADMIN'")]
