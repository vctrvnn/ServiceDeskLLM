from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import MessageCreateDTO
from app.database import get_db
from app.crud import create_message, get_dialog
from app.utils.logger import logger

router = APIRouter(prefix="/memory", tags=["chat"])


@router.post("/create_message")
async def create_message_endpoint(
    msg: MessageCreateDTO, db: AsyncSession = Depends(get_db)
):
    logger.debug(f"POST /create_message: {msg.json()}")
    try:
        new_msg = await create_message(msg=msg, db=db)
        return new_msg
    except Exception as e:
        logger.exception("Ошибка при создании сообщения")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_dialog/{dialog_id}")
async def get_dialog_endpoint(
    dialog_id: int, limit: int = 50, db: AsyncSession = Depends(get_db)
):
    logger.debug(f"GET /get_dialog/{dialog_id}, limit={limit}")
    try:
        return await get_dialog(dialog_id=dialog_id, limit=limit, db=db)
    except Exception as e:
        logger.exception("Ошибка при получении диалога")
        raise HTTPException(status_code=500, detail=str(e))
