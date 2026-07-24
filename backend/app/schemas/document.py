from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import BaseModel, ConfigDict

class DocumentUploadResponse(BaseModel):
    id: UUID
    filename: str
    message: str

class DocumentResponse(BaseModel):
    id: UUID
    user_id: UUID
    project_id: UUID

    filename: str
    file_type: str
    file_size: int
    storage_path: str

    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)