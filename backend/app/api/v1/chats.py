from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.chat import (
    ChatCreateRequest,
    ChatResponse,
    ChatListResponse,
    MessageResponse,
)
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/chats",
    tags=["Chats"],
)


@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_chat(
    request: ChatCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)

    chat = service.create_chat(
        title=request.title,
        user_id=current_user.id,
        project_id=request.project_id,
    )

    return chat


@router.get(
    "",
    response_model=list[ChatListResponse],
)
def list_chats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)

    return service.list_chats(
        user_id=current_user.id,
    )


@router.get(
    "/{chat_id}",
    response_model=list[MessageResponse],
)
def get_chat(
    chat_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)

    chat = service.get_chat(
        chat_id=chat_id,
        user_id=current_user.id,
    )

    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found.",
        )

    return service.get_chat_history(
        chat_id=chat_id,
    )


@router.delete(
    "/{chat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_chat(
    chat_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)

    deleted = service.delete_chat(
        chat_id=chat_id,
        user_id=current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found.",
        )

    return None