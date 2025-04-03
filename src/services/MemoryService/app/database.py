import subprocess
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.config import settings
from app.utils.logger import logger

DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_async_engine(
    url=DATABASE_URL, pool_size=10, max_overflow=20, echo=False, future=True
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            logger.debug("Открыта новая сессия к БД")
            yield session
        finally:
            await session.close()
            logger.debug("Закрыта сессия к БД")


def run_migrations():
    try:
        logger.info("Запуск alembic миграций...")
        result = subprocess.run(
            ["alembic", "upgrade", "head"], capture_output=True, text=True
        )
        if result.returncode != 0:
            logger.error(f"Alembic upgrade failed: {result.stderr}")
            raise RuntimeError(f"Alembic upgrade failed: {result.stderr}")
        if result.stdout:
            logger.debug(f"Alembic output: {result.stdout}")
        logger.info("Миграции выполнены успешно.")
    except Exception as e:
        logger.exception(f"Migration failed: {e}")
        raise
    finally:
        engine.dispose()
        logger.debug("Engine.dispose() вызван, соединения закрыты.")


class Base(DeclarativeBase):
    pass
