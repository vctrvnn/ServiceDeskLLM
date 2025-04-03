import os
import logging
import subprocess
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

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
            yield session
        finally:
            await session.close()


def run_migrations():
    try:
        logging.info("Starting database migrations")
        result = subprocess.run(
            ["alembic", "upgrade", "head"], capture_output=True, text=True
        )
        if result.returncode != 0:
            logging.error(f"Alembic upgrade failed: {result.stderr}")
            raise RuntimeError(f"Alembic upgrade failed: {result.stderr}")
        if result.stdout:
            logging.info(f"Alembic output: {result.stdout}")
        logging.info("Database migrations completed successfully")
    except Exception as e:
        logging.error(f"Migration failed: {e}")
        raise
    finally:
        engine.dispose()
        logging.info("Disposed of the engine to close all connections.")


class Base(DeclarativeBase):
    pass
