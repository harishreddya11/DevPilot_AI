from uuid import UUID
from pydantic import BaseModel, Field


class RetrievalRequest(BaseModel):
    project_id: UUID
    question: str = Field(..., min_length=3)
    limit: int = Field(default=5, ge=1, le=10)


class RetrievedChunk(BaseModel):
    document_id: UUID
    document_name: str
    chunk_index: int
    score: float
    content: str


class RetrievalResponse(BaseModel):
    question: str
    matches: list[RetrievedChunk]