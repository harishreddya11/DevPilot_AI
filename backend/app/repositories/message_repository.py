from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.message import Message
from app.repositories.base_repository import BaseRepository


class MessageRepository(BaseRepository[Message]):

    def __init__(self, db: Session):
        super().__init__(db)

    def create(
        self,
        chat_id,
        role: str,
        content: str,
    ) -> Message:

        message = Message(
            chat_id=chat_id,
            role=role,
            content=content,
        )

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    def list_by_chat(
        self,
        chat_id,
    ):

        stmt = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.created_at.asc())
        )

        return self.db.scalars(stmt).all()