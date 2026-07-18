import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.chat import Chat
from app.models.user import User
from app.schemas.chat import ChatCreate, ChatUpdate


class ChatService:
    def __init__(self, db: Session):
        self.db = db

    def create_chat(
        self,
        chat_data: ChatCreate,
        current_user: User,
    ) -> Chat:
        chat = Chat(
            title=chat_data.title,
            user_id=current_user.id,
        )

        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)

        return chat

    def get_chats(
        self,
        current_user: User,
    ) -> list[Chat]:
        return (
            self.db.query(Chat)
            .filter(Chat.user_id == current_user.id)
            .order_by(Chat.created_at.desc())
            .all()
        )

    def get_chat(
        self,
        chat_id: uuid.UUID,
        current_user: User,
    ) -> Chat:
        chat = (
            self.db.query(Chat)
            .filter(
                Chat.id == chat_id,
                Chat.user_id == current_user.id,
            )
            .first()
        )

        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )

        return chat

    def update_chat(
        self,
        chat_id: uuid.UUID,
        chat_data: ChatUpdate,
        current_user: User,
    ) -> Chat:
        chat = self.get_chat(chat_id, current_user)

        chat.title = chat_data.title

        self.db.commit()
        self.db.refresh(chat)

        return chat

    def delete_chat(
        self,
        chat_id: uuid.UUID,
        current_user: User,
    ) -> None:
        chat = self.get_chat(chat_id, current_user)

        self.db.delete(chat)
        self.db.commit()