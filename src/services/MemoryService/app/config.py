from pydantic_settings import BaseSettings, SettingsConfigDict

from app.utils.logger import logger


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        logger.debug(f"Сформирован DATABASE_URL_asyncpg: {url}")

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
logger.info("Конфиг загружен.")
