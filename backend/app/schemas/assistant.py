from uuid import UUID

from pydantic import BaseModel


class AssistantRequest(BaseModel):
    chat_id: UUID
    question: str


class AssistantResponse(BaseModel):
    answer: str