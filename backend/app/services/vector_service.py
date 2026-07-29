from uuid import UUID

from app.models.document_chunk import DocumentChunk
from app.repositories.document_repository import DocumentRepository
from app.services.embedding_service import EmbeddingService


class VectorService:
    """
    Handles embedding generation and semantic search.
    """

    def __init__(
        self,
        document_repository: DocumentRepository,
    ):
        self.document_repository = document_repository

    def generate_embeddings(
        self,
        chunks: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for document chunks.
        """
        return EmbeddingService.generate_embeddings(chunks)

    def search(
        self,
        *,
        project_id: UUID,
        query: str,
        top_k: int = 5,
    ) -> list[DocumentChunk]:
        """
        Perform semantic search over the user's document chunks.
        """

        if not query.strip():
            return []

        query_embedding = EmbeddingService.generate_embedding(query)

        return self.document_repository.search_similar_chunks(
            project_id=project_id,
            query_embedding=query_embedding,
            top_k=top_k,
        )