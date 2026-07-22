from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.message import Message
from app.repositories.base_repository import BaseRepository


class MessageRepository(BaseRepository[Message]):
    def __init__(self, db: Session):
        super().__init__(db)

    def create(
        self,
        *,
        chat_id: UUID,
        role: str,
        content: str,
    ) -> Message:
        """
        Create a new message.
        """
        message = Message(
            chat_id=chat_id,
            role=role,
            content=content,
        )

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    def get_by_id(
        self,
        message_id: UUID,
    ) -> Message | None:
        """
        Get a message by ID.
        """
        stmt = (
            select(Message)
            .where(Message.id == message_id)
        )

        return self.db.scalar(stmt)

    def list_by_chat(
        self,
        chat_id: UUID,
    ) -> list[Message]:
        """
        Get all messages for a chat.
        """
        stmt = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.created_at.asc())
        )

        return self.db.scalars(stmt).all()

    def delete(
        self,
        message: Message,
    ) -> None:
        """
        Delete a message.
        """
        self.db.delete(message)
        self.db.commit()

    def delete_by_chat(
        self,
        chat_id: UUID,
    ) -> None:
        """
        Delete all messages belonging to a chat.
        """
        messages = self.list_by_chat(chat_id)

        for message in messages:
            self.db.delete(message)

        self.db.commit()

    def commit(self) -> None:
        """
        Commit the current transaction.
        """
        self.db.commit()

    def rollback(self) -> None:
        """
        Rollback the current transaction.
        """
        self.db.rollback()

    def refresh(
        self,
        message: Message,
    ) -> None:
        """
        Refresh the message instance.
        """
        self.db.refresh(message)

    def get_recent_messages(
        self,
        chat_id: UUID,
        limit: int = 10,
    ) -> list[Message]:

        stmt = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )

        messages = self.db.scalars(stmt).all()

        return list(reversed(messages))