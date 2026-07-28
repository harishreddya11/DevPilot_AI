from app.models.document import Document
from app.parsers.parser_factory import ParserFactory
from app.repositories.document_repository import DocumentRepository
from app.services.chunk_service import ChunkingService
from app.services.embedding_service import EmbeddingService


class DocumentProcessingService:
    """
    Extract text, split into chunks, generate embeddings,
    and store them in the vector database.
    """

    def __init__(
        self,
        document_repository: DocumentRepository,
    ):
        self.document_repository = document_repository

    def extract_text(
        self,
        document: Document,
    ) -> str:
        """
        Extract text from the uploaded document.
        """

        parser = ParserFactory.get_parser(document.filename)

        return parser.extract_text(
            document.storage_path
        )

    def process_document(
        self,
        document: Document,
    ) -> dict:
        """
        Complete document processing pipeline.

        1. Extract text
        2. Chunk text
        3. Generate embeddings
        4. Store chunks
        """

        # Extract text
        text = self.extract_text(document)

        if not text.strip():
            raise ValueError(
                "No text could be extracted from the document."
            )

        # Chunk text
        # Chunk text
        chunk_service = ChunkingService(
            chunk_size=1000,
            chunk_overlap=200,
        )

        chunks = chunk_service.split_text(text)

        if not chunks:
            raise ValueError(
                "No chunks were generated from the document."
            )

        # Generate embeddings
        embeddings = EmbeddingService.generate_embeddings(
            chunks
        )

        # Store chunks + vectors
        self.document_repository.create_chunks(
            document_id=document.id,
            chunks=chunks,
            embeddings=embeddings,
        )

        # Commit chunk records
        self.document_repository.commit()

        return {
            "document_id": str(document.id),
            "characters": len(text),
            "total_chunks": len(chunks),
            "embedding_dimension": len(embeddings[0])
            if embeddings
            else 0,
        }