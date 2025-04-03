import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from app.config import settings
from app.clients.memory_service_client import MemoryServiceClient
from app.schemas import MessageCreateDTO
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
                role="user",
            )
        )
        await message.answer("Сообщение записано в базу данных!")
    except Exception as e:
        logger.exception("Ошибка при сохранении сообщения в MemoryService")
        await message.answer("Произошла ошибка при сохранении сообщения.")
        return


# @dp.message(Text())  # Хендлер на любое текстовое сообщение
# async def on_text_message(message: Message):
#     user_id = message.from_user.id
#     text = message.text

#     # Отправляем в MemoryService (create_message)
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.post(
#                 url=f"{settings.MEMORY_SERVICE_URL}/memory/create_message",
#                 json={
#                     "dialog_id": 123,  # Пример, под вашу логику
#                     "user_id": user_id,
#                     "role": "USER",
#                     "message_content": text,
#                 },
#             )
#             response.raise_for_status()
#         logger.info(f"Сообщение пользователя {user_id} сохранено в MemoryService.")
#     except Exception as e:
#         logger.exception("Ошибка при сохранении сообщения в MemoryService")
#         await message.answer("Произошла ошибка при сохранении сообщения.")
#         return

#     # Отвечаем пользователю
#     await message.answer(f"Получено сообщение: <b>{text}</b>")


def run_long_polling_bot():
    logger.info("Запуск бота (Long Polling) ...")
    asyncio.run(dp.start_polling(bot))
