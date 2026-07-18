import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MessageCreate(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=10000,
    )


class MessageResponse(BaseModel):
    id: uuid.UUID
    role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatConversationResponse(BaseModel):
    user_message: MessageResponse
    assistant_message: MessageResponse