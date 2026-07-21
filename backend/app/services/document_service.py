import os
import uuid

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.document import Document
from app.schemas.document import DocumentResponse


class DocumentService:

    def __init__(self, db: Session):
        self.db = db
        self.settings = get_settings()

    def upload_document(
        self,
        user_id: uuid.UUID,
        file: UploadFile,
    ) -> DocumentResponse:

        # Validate extension
        extension = os.path.splitext(file.filename)[1].lower()

        if extension not in self.settings.allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type.",
            )

        # Create upload directory
        os.makedirs(
            self.settings.upload_directory,
            exist_ok=True,
        )

        # Generate unique filename
        unique_name = f"{uuid.uuid4()}{extension}"

        file_path = os.path.join(
            self.settings.upload_directory,
            unique_name,
        )

        # Save file
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        # Save metadata
        document = Document(
            user_id=user_id,
            filename=file.filename,
            file_path=file_path,
            content_type=file.content_type,
        )

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        return DocumentResponse.model_validate(document)