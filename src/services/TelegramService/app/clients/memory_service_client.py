import httpx
from app.utils.logger import logger
from app.schemas import MessageCreateDTO


class MemoryServiceClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def create_message(self, data: MessageCreateDTO):
        endpoint_url = f"{self.base_url}/memory/create_message"
        async with httpx.AsyncClient() as async_client:
            response = await async_client.post(url=endpoint_url, json=data.model_dump())
            response.raise_for_status()
        logger.info(
            f"Успешно сохранили сообщение пользователя {data.user_id} в MemoryService."
        )
        return response.json()
