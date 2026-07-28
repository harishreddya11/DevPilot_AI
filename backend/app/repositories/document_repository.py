from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.models.document import Document
from app.models.document_chunk import DocumentChunk


class DocumentRepository:
    """
    Repository responsible for document database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_document(
        self,
        *,
        user_id: UUID,
        project_id: UUID,
        filename: str,
        file_type: str,
        file_size: int,
        storage_path: str,
    ) -> Document:

        document = Document(
            user_id=user_id,
            project_id=project_id,
            filename=filename,
            file_type=file_type,
            file_size=file_size,
            storage_path=storage_path,
        )

        self.db.add(document)
        self.db.flush()

        return document

    def create_chunks(
        self,
        *,
        document_id: UUID,
        chunks: list[str],
        embeddings: list[list[float]],
    ) -> None:

        document_chunks = []

        for index, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):
            document_chunks.append(
                DocumentChunk(
                    document_id=document_id,
                    chunk_index=index,
                    content=chunk,
                    embedding=embedding,
                )
            )

        self.db.add_all(document_chunks)

    def get_document(
        self,
        document_id: UUID,
    ) -> Document | None:

        return self.db.get(
            Document,
            document_id,
        )

    def get_document_chunks(
        self,
        document_id: UUID,
    ) -> list[DocumentChunk]:

        return (
            self.db.query(DocumentChunk)
            .filter(
                DocumentChunk.document_id == document_id
            )
            .order_by(
                DocumentChunk.chunk_index.asc()
            )
            .all()
        )

    def search_similar_chunks(
        self,
        *,
        user_id: UUID,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[DocumentChunk]:
        """
        Perform semantic search across all documents belonging
        to the given user.
        """

        return (
            self.db.query(DocumentChunk)
            .options(
                joinedload(DocumentChunk.document)
            )
            .join(
                Document,
                Document.id == DocumentChunk.document_id,
            )
            .filter(
                Document.user_id == user_id,
            )
            .order_by(
                DocumentChunk.embedding.cosine_distance(
                    query_embedding
                )
            )
            .limit(top_k)
            .all()
        )

    def delete_document(
        self,
        document_id: UUID,
    ) -> None:

        document = self.get_document(document_id)

        if document:
            self.db.delete(document)

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()

    def refresh(
        self,
        document: Document,
    ) -> None:
        self.db.refresh(document)