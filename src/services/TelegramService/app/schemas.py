from pydantic import BaseModel
import datetime


class MessageCreateDTO(BaseModel):
    dialog_id: int
    user_id: int
    role: str
    message_content: str


class MessageReadDTO(MessageCreateDTO):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
