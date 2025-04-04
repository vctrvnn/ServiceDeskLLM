from enum import Enum


class RoleEnum(str, Enum):
    USER = "user"
    AI = "ai"
    SYSTEM = "system"
    TOOL = "tool"