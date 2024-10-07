import logging


def get_logger():
    logger = logging.getLogger("bot")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s::%(levelname)s - %(message)s")
    handler = logging.FileHandler("bot_logs.log")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


bot_logger = get_logger()
