import os

ADMIN_PASS = os.environ.get("ADMIN_PASS", "123")
TOKEN = os.environ.get("TOKEN")
DB_NAME = os.environ.get("DB_NAME")
CHANNEL_ID = os.environ.get("CHANNEL_ID", -1002269031953)

ADMIN_START_MESSAGE = os.environ.get("DB_NAME", "Розыгрыши:")
USER_START_MESSAGE = os.environ.get("DB_NAME", "Привет! Этот бот пришлет тебе результаты розыгрыша")
