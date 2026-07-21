from uuid import UUID

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk


class DocumentRepository:
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
        document_id: UUID,
        chunks: list[str],
        embeddings: list[list[float]],
    ) -> None:

        document_chunks = [
            DocumentChunk(
                document_id=document_id,
                chunk_index=index,
                content=chunk,
                embedding=embedding,
            )
            for index, (chunk, embedding) in enumerate(
                zip(chunks, embeddings)
            )
        ]

        self.db.add_all(document_chunks)

    def get_document(
        self,
        document_id: UUID,
    ) -> Document | None:

        return self.db.get(Document, document_id)

    def get_document_chunks(
        self,
        document_id: UUID,
    ) -> list[DocumentChunk]:

        return (
            self.db.query(DocumentChunk)
            .filter(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index)
            .all()
        )

    def commit(self) -> None:
        self.db.commit()

    def refresh(self, document: Document) -> None:
        self.db.refresh(document)