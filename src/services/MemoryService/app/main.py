from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from contextlib import asynccontextmanager

from app.router import router as memory_router
from app.database import run_migrations

import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        run_migrations()
        yield
    except Exception as e:
        logging.error(f"Ошибка при запуске приложения: {e}")
        raise
    finally:
        logging.info("Завершение работы приложения.")


app = FastAPI(title="Memory Service", version="1.0.0", lifespan=lifespan)


@app.get("/", tags=['docs'])
async def redirect():
    return RedirectResponse(url="/docs")


app.include_router(memory_router)
