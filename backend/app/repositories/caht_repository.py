from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chat import Chat
from app.repositories.base_repository import BaseRepository


class ChatRepository(BaseRepository[Chat]):

    def __init__(self, db: Session):
        super().__init__(db)

    def create(
        self,
        title: str,
        user_id,
    ) -> Chat:

        chat = Chat(
            title=title,
            user_id=user_id,
        )

        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)

        return chat

    def list_by_user(
        self,
        user_id,
    ):

        stmt = (
            select(Chat)
            .where(Chat.user_id == user_id)
            .order_by(Chat.created_at.desc())
        )

        return self.db.scalars(stmt).all()