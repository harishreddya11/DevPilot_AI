from uuid import UUID

from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.repositories.document_repository import DocumentRepository
from app.services.embedding_service import EmbeddingService


class VectorService:
    """
    Service responsible for semantic vector search.
    """

    def __init__(
        self,
        db: Session,
        embedding_service: EmbeddingService,
    ):
        self.embedding_service = embedding_service
        self.repository = DocumentRepository(db)

    async def search(
        self,
        *,
        user_id: UUID,
        query: str,
        top_k: int = 5,
    ) -> list[DocumentChunk]:
        """
        Generate an embedding for the query and return
        the most relevant document chunks.
        """

        if not query.strip():
            return []

        query_embedding = (
            await self.embedding_service.generate_embedding(
                query
            )
        )

        return self.repository.search_similar_chunks(
            user_id=user_id,
            query_embedding=query_embedding,
            top_k=top_k,
        )