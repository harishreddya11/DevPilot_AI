from pathlib import Path
from uuid import uuid4
from uuid import UUID
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session
from app.repositories.document_repository import DocumentRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.document import DocumentResponse
from app.api.dependencies.auth import get_current_user
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.schemas.document import DocumentUploadResponse
from app.services.chunk_service import ChunkingService
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.document_processing_service import DocumentProcessingService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

UPLOAD_DIR = Path(settings.upload_directory)
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


@router.get("/{document_id}/extract")
def extract_document(
    document_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document_repository = DocumentRepository(db)

    document = document_repository.get_by_id(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    processor = DocumentProcessingService(
        document_repository=document_repository,
    )

    text = processor.extract_text(document)

    return {
        "document": document.filename,
        "characters": len(text),
        "preview": text[:1000],
    }

@router.post(
    "/{project_id}/documents",
    response_model=DocumentResponse,
    status_code=201,
)
def upload_document(
    project_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document_repository = DocumentRepository(db)
    project_repository = ProjectRepository(db)

    processing_service = DocumentProcessingService(
        document_repository=document_repository,
    )

    service = DocumentService(
        document_repository=document_repository,
        project_repository=project_repository,
        document_processing_service=processing_service,
    )

    return service.upload_document(
        project_id=project_id,
        user_id=current_user.id,
        file=file,
    )

@router.get("/{document_id}/test-processing")
def test_processing(
    document_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document_repository = DocumentRepository(db)

    document = document_repository.get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    if document.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )

    processor = DocumentProcessingService(
        document_repository=document_repository,
    )

    text = processor.extract_text(document)
    chunk_service = ChunkingService(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = chunk_service.split_text(text)

    embeddings = EmbeddingService.generate_embeddings(chunks)

    return {
        "filename": document.filename,
        "characters": len(text),
        "total_chunks": len(chunks),
        "embedding_dimension": len(embeddings[0]) if embeddings else 0,
        "sample_chunk": chunks[0] if chunks else "",
        "sample_embedding": embeddings[0][:10] if embeddings else []
    }