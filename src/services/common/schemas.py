from .enum import RoleEnum

from pydantic import BaseModel, ConfigDict
import datetime

class MessageCreateDTO(BaseModel):
    dialog_id: int
    user_id: int
    role: RoleEnum
    message_content: str

    model_config = ConfigDict(
        use_enum_values=True
    )

class MessageReadDTO(MessageCreateDTO):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True