import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from app.config import settings
from app.clients.memory_service_client import MemoryServiceClient
from app.schemas import MessageCreateDTO
from app.common.enum import RoleEnum
from app.config import settings
from app.utils.logger import logger

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

ms_client = MemoryServiceClient(base_url=settings.MEMORY_SERVICE_URL)


@dp.message(F.text)
async def cmd_start(message: Message, ms_client: MemoryServiceClient = ms_client):
    try:
        ms_response = await ms_client.create_message(
            data=MessageCreateDTO(
                dialog_id=message.from_user.id,
                user_id=message.from_user.id,
                message_content=message.text,
                role=RoleEnum.USER,
            )
        )
        await message.answer("Сообщение записано в базу данных!")
    except Exception as e:
        logger.exception("Ошибка при сохранении сообщения в MemoryService")
        await message.answer("Произошла ошибка при сохранении сообщения.")
        return


def run_long_polling_bot():
    logger.info("Запуск бота (Long Polling) ...")
    asyncio.run(dp.start_polling(bot))
