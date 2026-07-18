import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.message import (
    ChatConversationResponse,
    MessageCreate,
)
from app.services.message_service import MessageService

router = APIRouter(
    prefix="/chats",
    tags=["Messages"],
)


@router.post(
    "/{chat_id}/messages",
    response_model=ChatConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
def send_message(
    chat_id: uuid.UUID,
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MessageService(db)

    return service.send_message(
        chat_id=chat_id,
        message_data=message,
        current_user=current_user,
    )