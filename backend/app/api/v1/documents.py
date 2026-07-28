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

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

UPLOAD_DIR = Path(settings.upload_directory)
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


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
            detail=f"Unsupported file type: {extension}",
        )

    unique_filename = f"{uuid4()}{extension}"

    file_path = UPLOAD_DIR / unique_filename

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    service = DocumentService(
        db=db,
        chunk_service=ChunkingService(),
        embedding_service=EmbeddingService(),
    )

    document = await service.process_document(
        user_id=current_user.id,
        filename=file.filename,
        file_path=str(file_path),
        content_type=file.content_type
        or "application/octet-stream",
    )

    return DocumentUploadResponse(
        id=document.id,
        filename=document.filename,
        message="Document uploaded successfully.",
    )

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

    service = DocumentService(
        document_repository,
        project_repository,
    )

    return service.upload_document(
        project_id=project_id,
        user_id=current_user.id,
        file=file,
    )