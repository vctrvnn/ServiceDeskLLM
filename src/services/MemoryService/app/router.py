from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import MessageCreateDTO, MessageReadDTO
from app.database import get_db
from app.crud import create_message, get_dialog

router = APIRouter(prefix="/memory", tags=["chat"])


@router.post("/create_message")
async def create_message_endpoint(
    msg: MessageCreateDTO, db: AsyncSession = Depends(get_db)
):
    try:
        return await create_message(msg=msg, db=db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_dialog/{dialog_id}")
async def get_dialog_endpoint(
    dialog_id: int, limit: int = 50, db: AsyncSession = Depends(get_db)
):
    try:
        return await get_dialog(dialog_id=dialog_id, limit=limit, db=db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
