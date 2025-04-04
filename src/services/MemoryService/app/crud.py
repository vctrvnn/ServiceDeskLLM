from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from app.models import ChatMessage
from app.schemas import MessageCreateDTO, MessageReadDTO
from app.utils.logger import logger


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
        if not messages:
            logger.warning(f"Сообщений по диалогу {dialog_id} не найдено")
        logger.info(f"Загружено {len(messages)} сообщений по диалогу {dialog_id}")
        return messages
    except Exception:
        logger.exception("Ошибка при загрузке диалога")
        raise


async def extend_dialog(msg: MessageCreateDTO, db: AsyncSession) -> dict:
    logger.debug(
        f"Создание сообщения в БД: dialog_id={msg.dialog_id}, user_id={msg.user_id}, role={msg.role}"
    )
    orm_msg = ChatMessage(**msg.model_dump())
    db.add(orm_msg)
    try:
        await db.commit()
        await db.refresh(orm_msg)
        logger.info(f"Сообщение сохранено в БД, id={orm_msg.id}")
        return {"status": "success", "message": " Сообщение успешно сохранено"}
    except Exception:
        logger.exception(
            f"Ошибка при сохранении сообщения в БД dialog_id={msg.dialog_id}"
        )
        await db.rollback()
        raise


async def clear_dialog(dialog_id: int, db: AsyncSession) -> dict:
    logger.debug(f"Удаление истории диалога dialog_id={dialog_id}")
    try:
        stmt = delete(ChatMessage).where(ChatMessage.dialog_id == dialog_id)
        result = await db.execute(stmt)
        await db.commit()
        logger.info(f"Удалено сообщений: {result.rowcount} из диалога {dialog_id}")
        return {"status": "success", "deleted": f"Удалено: {result.rowcount} сообщений"}
    except Exception:
        logger.exception(
            f"Ошибка при bulk удалении истории диалога dialog_id={dialog_id}"
        )
        await db.rollback()
        raise
