import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.chat import ChatCreate, ChatResponse, ChatUpdate
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/chats",
    tags=["Chats"],
)


@router.post(
    "/",
    response_model=ChatResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_chat(
    chat_data: ChatCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)
    return service.create_chat(chat_data, current_user)


@router.get(
    "/",
    response_model=list[ChatResponse],
)
def get_chats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)
    return service.get_chats(current_user)


@router.get(
    "/{chat_id}",
    response_model=ChatResponse,
)
def get_chat(
    chat_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)
    return service.get_chat(chat_id, current_user)


@router.patch(
    "/{chat_id}",
    response_model=ChatResponse,
)
def update_chat(
    chat_id: uuid.UUID,
    chat_data: ChatUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)
    return service.update_chat(chat_id, chat_data, current_user)


@router.delete(
    "/{chat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_chat(
    chat_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)
    service.delete_chat(chat_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)