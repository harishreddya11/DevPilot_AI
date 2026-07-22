from uuid import UUID

from sqlalchemy.orm import Session

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
        filename: str,
        file_path: str,
        content_type: str,
    ) -> Document:

        document = Document(
            user_id=user_id,
            filename=filename,
            file_path=file_path,
            content_type=content_type,
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
                DocumentChunk.chunk_index
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

        return (
            self.db.query(DocumentChunk)
            .join(
                Document,
                Document.id == DocumentChunk.document_id,
            )
            .filter(
                Document.user_id == user_id
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
    ):

        document = self.get_document(document_id)

        if document:
            self.db.delete(document)

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def refresh(
        self,
        document: Document,
    ):
        self.db.refresh(document)