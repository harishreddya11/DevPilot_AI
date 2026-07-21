from uuid import UUID

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.chunk_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.utils.pdf_parser import PDFParser


class DocumentService:
    def __init__(
        self,
        db: Session,
        chunk_service: ChunkingService,
        embedding_service: EmbeddingService,
    ):
        self.db = db
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
        """
        Process an uploaded document:
        1. Save document metadata.
        2. Extract text from the PDF.
        3. Split text into chunks.
        4. Generate embeddings.
        5. Save chunks with embeddings.
        """

        try:
            # Save document metadata
            document = Document(
                user_id=user_id,
                filename=filename,
                file_path=file_path,
                content_type=content_type,
            )

            self.db.add(document)
            self.db.flush()

            # Extract text from PDF
            text = PDFParser.extract_text(file_path)

            if not text or not text.strip():
                raise ValueError("No text found in the uploaded PDF.")

            # Split into chunks
            chunks = self.chunk_service.split(text)

            if not chunks:
                raise ValueError("Failed to generate text chunks.")

            # Generate embeddings
            embeddings = await self.embedding_service.embed_documents(chunks)

            if len(chunks) != len(embeddings):
                raise ValueError(
                    "Number of embeddings does not match number of chunks."
                )

            # Create document chunks
            document_chunks = [
                DocumentChunk(
                    document_id=document.id,
                    chunk_index=index,
                    content=chunk,
                    embedding=embedding,
                )
                for index, (chunk, embedding) in enumerate(
                    zip(chunks, embeddings)
                )
            ]

            self.db.add_all(document_chunks)

            self.db.commit()
            self.db.refresh(document)

            return document

        except Exception:
            self.db.rollback()
            raise