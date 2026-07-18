from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, request: RegisterRequest) -> UserResponse:
        """
        Register a new user.
        """

        existing_user = (
            self.db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if existing_user:
            raise ValueError("Email already registered")

        user = User(
            full_name=request.full_name,
            email=request.email,
            hashed_password=hash_password(request.password),
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return UserResponse.model_validate(user)

    def login(self, request: LoginRequest) -> TokenResponse:
        """
        Authenticate a user.
        """

        user = (
            self.db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if not user:
            raise ValueError("Invalid email or password")

        if not verify_password(
            request.password,
            user.hashed_password,
        ):
            raise ValueError("Invalid email or password")

        access_token = create_access_token(
            subject=str(user.id),
        )

        return TokenResponse(
            access_token=access_token,
        )