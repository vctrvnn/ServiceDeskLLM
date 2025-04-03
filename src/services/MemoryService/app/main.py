from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

from app.router import router as memory_router
from app.database import run_migrations
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Запуск миграций при старте приложения...")
        run_migrations()
        logger.info("Миграции успешно выполнены.")
        yield
    except Exception as e:
        logger.exception(f"Ошибка при запуске приложения: {e}")
        raise
    finally:
        logger.info("Завершение работы приложения.")


app = FastAPI(title="Memory Service", version="1.0.0", lifespan=lifespan)


@app.get("/", tags=["docs"])
async def redirect():
    logger.debug("Редирект на /docs")
    return RedirectResponse(url="/docs")


app.include_router(memory_router)
