from pydantic_settings import BaseSettings, SettingsConfigDict
from app.utils.logger import logger


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    MEMORY_SERVICE_URL: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
logger.info("Конфиг TelegramService загружен.")
