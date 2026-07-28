from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chat import Chat
from app.repositories.base_repository import BaseRepository


class ChatRepository(BaseRepository[Chat]):
    def __init__(self, db: Session):
        super().__init__(db)

    def create(
        self,
        *,
        title: str,
        user_id: UUID,
    ) -> Chat:
        """
        Create a new chat.
        """
        chat = Chat(
            title=title,
            user_id=user_id,
        )

        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)

        return chat

    def get_by_id(
        self,
        chat_id: UUID,
    ) -> Chat | None:
        """
        Get chat by ID.
        """
        stmt = select(Chat).where(Chat.id == chat_id)

        return self.db.scalar(stmt)

    def get_user_chat(
        self,
        *,
        chat_id: UUID,
        user_id: UUID,
    ) -> Chat | None:
        """
        Get a chat belonging to a specific user.
        """
        stmt = (
            select(Chat)
            .where(Chat.id == chat_id)
            .where(Chat.user_id == user_id)
        )

        return self.db.scalar(stmt)

    def list_by_user(
        self,
        user_id: UUID,
    ) -> list[Chat]:
        """
        List all chats for a user.
        """
        stmt = (
            select(Chat)
            .where(Chat.user_id == user_id)
            .order_by(Chat.created_at.desc())
        )

        return self.db.scalars(stmt).all()

    def update_title(
        self,
        *,
        chat: Chat,
        title: str,
    ) -> Chat:
        """
        Update chat title.
        """
        chat.title = title

        self.db.commit()
        self.db.refresh(chat)

        return chat

    def delete(
        self,
        chat: Chat,
    ) -> None:
        """
        Delete a chat.
        """
        self.db.delete(chat)
        self.db.commit()

    def commit(self) -> None:
        """
        Commit current transaction.
        """
        self.db.commit()

    def rollback(self) -> None:
        """
        Rollback current transaction.
        """
        self.db.rollback()

    def refresh(
        self,
        chat: Chat,
    ) -> None:
        """
        Refresh chat instance.
        """
        self.db.refresh(chat)