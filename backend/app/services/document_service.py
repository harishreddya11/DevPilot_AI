from uuid import UUID

from sqlalchemy.orm import Session

from app.models.document import Document
from app.parsers.parser_factory import ParserFactory
from app.repositories.document_repository import (
    DocumentRepository,
)
from app.services.chunk_service import ChunkingService
from app.services.embedding_service import EmbeddingService


class DocumentService:

    def __init__(
        self,
        db: Session,
        chunk_service: ChunkingService,
        embedding_service: EmbeddingService,
    ):
        self.repository = DocumentRepository(db)
        self.chunk_service = chunk_service
        self.embedding_service = embedding_service

    async def process_document(
        self,
        *,
        user_id: UUID,
        filename: str,
        file_path: str,
        content_type: str,
    ) -> Document:

        try:

            # Select parser
            parser = ParserFactory.get_parser(filename)

            # Extract text
            text = parser.extract_text(file_path)

            if not text:
                raise ValueError(
                    "Document is empty."
                )

            text = text.strip()

            if not text:
                raise ValueError(
                    "No readable text found."
                )

            # Save document
            document = self.repository.create_document(
                user_id=user_id,
                filename=filename,
                file_path=file_path,
                content_type=content_type,
            )

            # Chunk document
            chunks = self.chunk_service.split(text)

            if not chunks:
                raise ValueError(
                    "Failed to create chunks."
                )

            # Generate embeddings
            embeddings = (
                await self.embedding_service.embed_documents(
                    chunks
                )
            )

            if len(chunks) != len(embeddings):
                raise ValueError(
                    "Embedding count mismatch."
                )

            # Save chunks
            self.repository.create_chunks(
                document_id=document.id,
                chunks=chunks,
                embeddings=embeddings,
            )

            self.repository.commit()

            self.repository.refresh(document)

            return document

        except Exception:
            self.repository.rollback()
            raise