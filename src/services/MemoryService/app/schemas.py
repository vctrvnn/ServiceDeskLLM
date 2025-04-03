from pydantic import BaseModel
import datetime

from app.utils.enum import RoleEnum


class MessageCreateDTO(BaseModel):
    dialog_id: int
    user_id: int
    role: RoleEnum
    message_content: str


class MessageReadDTO(MessageCreateDTO):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True
