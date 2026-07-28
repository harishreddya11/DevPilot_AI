from uuid import UUID

from pydantic import BaseModel


class AssistantRequest(BaseModel):
    chat_id: UUID
    question: str


class Source(BaseModel):
    document: str
    chunk_index: int


class AssistantResponse(BaseModel):
    answer: str
    sources: list[Source]