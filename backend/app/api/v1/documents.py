from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.schemas.document import DocumentUploadResponse
from app.services.chunk_service import ChunkingService
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

UPLOAD_DIR = Path(settings.upload_directory)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    extension = Path(file.filename).suffix.lower()

    if extension not in settings.allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type.",
        )

    unique_filename = f"{uuid4()}{extension}"
    file_path = UPLOAD_DIR / unique_filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    service = DocumentService(
        db=db,
        chunk_service=ChunkingService(),
        embedding_service=EmbeddingService(),
    )

    document = await service.process_document(
        user_id=current_user.id,
        filename=file.filename,
        file_path=str(file_path),
        content_type=file.content_type or "application/octet-stream",
    )

    return DocumentUploadResponse(
        id=document.id,
        filename=document.filename,
        message="Document uploaded successfully.",
    )