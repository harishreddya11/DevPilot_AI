from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.assistant import (
    AssistantRequest,
    AssistantResponse,
)
from app.services.assistant_service import AssistantService

router = APIRouter(
    prefix="/assistant",
    tags=["Assistant"],
)


@router.post(
    "/chat",
    response_model=AssistantResponse,
)
async def chat(
    request: AssistantRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Ask a question about uploaded documents.
    """

    assistant = AssistantService(db)

    response = await assistant.ask(
        user_id=current_user.id,
        chat_id=request.chat_id,
        question=request.question,
    )

    return AssistantResponse(**response)