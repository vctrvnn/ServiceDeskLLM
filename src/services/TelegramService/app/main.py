from app.telegram_bot import run_long_polling_bot
from app.utils.logger import logger


if __name__ == "__main__":
    logger.info("TelegramService стартует...")
    run_long_polling_bot()
