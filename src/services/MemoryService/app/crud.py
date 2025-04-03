from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import ChatMessage
from app.schemas import MessageCreateDTO
from app.utils.logger import logger


async def create_message(msg: MessageCreateDTO, db: AsyncSession) -> ChatMessage:
    logger.debug(
        f"Создание сообщения в БД: dialog_id={msg.dialog_id}, user_id={msg.user_id}, role={msg.role}"
    )
    orm_msg = ChatMessage(**msg.model_dump())
    db.add(orm_msg)
    try:
        await db.commit()
        await db.refresh(orm_msg)
        logger.info(f"Сообщение сохранено в БД, id={orm_msg.id}")
        return orm_msg
    except Exception:
        logger.exception("Ошибка при сохранении сообщения в БД")
        await db.rollback()
        raise


async def get_dialog(dialog_id: int, limit: int, db: AsyncSession) -> list[ChatMessage]:
    logger.debug(f"Загрузка диалога dialog_id={dialog_id}, limit={limit}")
    query = (
        select(ChatMessage)
        .where(ChatMessage.dialog_id == dialog_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(limit)
    )
    try:
        result = await db.execute(query)
        messages = result.scalars().all()
        logger.info(f"Загружено {len(messages)} сообщений по диалогу {dialog_id}")
        return messages
    except Exception:
        logger.exception("Ошибка при загрузке диалога")
        raise
