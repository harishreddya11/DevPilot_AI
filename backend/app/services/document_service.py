from pathlib import Path
from uuid import UUID

from fastapi import HTTPException, UploadFile, status

from app.models.document import Document
from app.repositories.document_repository import DocumentRepository
from app.repositories.project_repository import ProjectRepository
from app.services.document_processing_service import DocumentProcessingService


class DocumentService:
    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".txt",
        ".md",
        ".py",
        ".java",
        ".js",
        ".ts",
        ".json",
        ".yaml",
        ".yml",
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".tiff",
        ".webp",
    }

    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

    def __init__(
        self,
        document_repository: DocumentRepository,
        project_repository: ProjectRepository,
        document_processing_service: DocumentProcessingService,
    ):
        self.document_repository = document_repository
        self.project_repository = project_repository
        self.document_processing_service = document_processing_service

    def upload_document(
        self,
        *,
        project_id: UUID,
        user_id: UUID,
        file: UploadFile,
    ) -> Document:

        # Validate project ownership
        project = self.project_repository.get_by_id(project_id)

        if project is None or project.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found.",
            )

        # Validate extension
        extension = Path(file.filename).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type.",
            )

        # Read file
        content = file.file.read()

        # Validate size
        if len(content) > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size exceeds 20 MB.",
            )

        # Save file
        storage_dir = Path("storage") / "projects" / str(project_id)
        storage_dir.mkdir(parents=True, exist_ok=True)

        storage_path = storage_dir / file.filename

        with open(storage_path, "wb") as f:
            f.write(content)

        # Create database record
        document = self.document_repository.create_document(
            user_id=user_id,
            project_id=project_id,
            filename=file.filename,
            file_type=extension,
            file_size=len(content),
            storage_path=str(storage_path),
        )

        self.document_repository.commit()
        self.document_repository.refresh(document)

        # Process document
        self.document_processing_service.process_document(document)

        return document