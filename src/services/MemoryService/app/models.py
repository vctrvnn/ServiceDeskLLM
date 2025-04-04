from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text

from app.database import Base
from app.common.enum import RoleEnum  # proxy import from --> src/services/common

import datetime


class ChatMessage(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    dialog_id: Mapped[int]
    user_id: Mapped[int]
    role: Mapped[RoleEnum]
    message_content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    )
