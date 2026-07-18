from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):

    def __init__(self, db: Session):
        super().__init__(db)

    def create(
        self,
        full_name: str,
        email: str,
        hashed_password: str,
    ) -> User:

        user = User(
            full_name=full_name,
            email=email,
            hashed_password=hashed_password,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_by_email(
        self,
        email: str,
    ) -> User | None:

        stmt = select(User).where(User.email == email)

        return self.db.scalar(stmt)

    def get_by_id(
        self,
        user_id,
    ) -> User | None:

        stmt = select(User).where(User.id == user_id)

        return self.db.scalar(stmt)