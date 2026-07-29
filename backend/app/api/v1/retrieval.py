from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.document_repository import DocumentRepository
from app.schemas.retrieval import (
    RetrievalRequest,
    RetrievalResponse,
    RetrievedChunk,
)
from app.services.vector_service import VectorService

router = APIRouter(
    prefix="/retrieval",
    tags=["Retrieval"],
)


@router.post(
    "/search",
    response_model=RetrievalResponse,
)
def search_documents(
    request: RetrievalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    repository = DocumentRepository(db)

    service = VectorService(repository)

    chunks = service.search(
        user_id=current_user.id,
        query=request.question,
        top_k=request.top_k,
    )

    matches = []

    for chunk in chunks:
        matches.append(
            RetrievedChunk(
                document_id=chunk.document_id,
                document_name=chunk.document.filename,
                chunk_index=chunk.chunk_index,
                score=None,
                content=chunk.content,
            )
        )

    return RetrievalResponse(
        question=request.question,
        matches=matches,
    )