from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.models.document_chunk import DocumentChunk


class VectorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def search_similar_chunks(
        self,
        project_id: UUID,
        query_embedding: list[float],
        limit: int = 5,
    ):
        stmt = (
            select(DocumentChunk)
            .join(Document)
            .where(Document.project_id == project_id)
            .order_by(
                DocumentChunk.embedding.cosine_distance(query_embedding)
            )
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()