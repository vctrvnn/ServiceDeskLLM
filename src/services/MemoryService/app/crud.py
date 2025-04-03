from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import ChatMessage
from app.schemas import MessageCreateDTO


async def create_message(msg: MessageCreateDTO, db: AsyncSession) -> ChatMessage:
    orm_msg = ChatMessage(**msg.model_dump())
    db.add(orm_msg)
    await db.commit()
    await db.refresh(orm_msg)
    return orm_msg


async def get_dialog(dialog_id: int, limit: int, db: AsyncSession) -> list[ChatMessage]:
    query = (
        select(ChatMessage)
        .where(ChatMessage.dialog_id == dialog_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().all()
