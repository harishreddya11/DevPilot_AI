import uuid

from pydantic import BaseModel, ConfigDict, Field


class ChatCreate(BaseModel):
    title: str = Field(
        default="New Chat",
        max_length=255,
    )


class ChatUpdate(BaseModel):
    title: str = Field(
        max_length=255,
    )


class ChatResponse(BaseModel):
    id: uuid.UUID
    title: str

    model_config = ConfigDict(from_attributes=True)