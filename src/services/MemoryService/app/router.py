from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import MessageCreateDTO, MessageReadDTO
from app.database import get_db
from app.crud import extend_dialog, get_dialog, clear_dialog
from app.utils.logger import logger

router = APIRouter(prefix="/memory", tags=["chat"])


@router.post("/create_message")
async def create_message_endpoint(
    msg: MessageCreateDTO, db: AsyncSession = Depends(get_db)
) -> dict:
    logger.debug(f"POST /create_message: {msg.model_dump()}")
    try:
        new_msg = await extend_dialog(msg=msg, db=db)
        return new_msg
    except Exception as e:
        logger.exception(f"Ошибка при создании сообщения: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_dialog/{dialog_id}")
async def get_dialog_endpoint(
    dialog_id: int, limit: int = 50, db: AsyncSession = Depends(get_db)
) -> list[MessageReadDTO]:
    logger.debug(f"GET /get_dialog/{dialog_id}, limit={limit}")
    try:
        messages_list = await get_dialog(dialog_id=dialog_id, limit=limit, db=db)
        return [MessageReadDTO.model_validate(msg_item) for msg_item in messages_list]
    except Exception as e:
        logger.exception(f"Ошибка при получении диалога: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clear_dialog/{dialog_id}")
async def clear_dialog_endpoint(
    dialog_id: int, db: AsyncSession = Depends(get_db)
) -> dict:
    logger.debug(f"DELETE /clear_dialog/{dialog_id}")
    try:
        result = await clear_dialog(dialog_id=dialog_id, db=db)
        return result
    except Exception as e:
        logger.exception(f"Ошибка при очистке диалога: {e}")
        raise HTTPException(status_code=500, detail=str(e))
