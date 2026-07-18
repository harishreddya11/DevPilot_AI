from sqlalchemy.orm import Session
from app.core.exceptions import ConflictError
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)
from app.core.exceptions import (
    AuthenticationError,
    ConflictError,
)


class AuthService:

    def __init__(self, db: Session):
        self.users = UserRepository(db)

    def register(
        self,
        request: RegisterRequest,
    ):

        existing = self.users.get_by_email(request.email)

        if existing:
           raise ConflictError("Email already exists")

        user = self.users.create(
            full_name=request.full_name,
            email=request.email,
            hashed_password=hash_password(request.password),
        )

        return user

    def login(
        self,
        request: LoginRequest,
    ) -> TokenResponse:

        user = self.users.get_by_email(request.email)

        if not user:
            raise AuthenticationError("Invalid credentials")

        if not verify_password(
            request.password,
            user.hashed_password,
        ):
           raise AuthenticationError("Invalid credentials")

        token = create_access_token(str(user.id))

        return TokenResponse(
            access_token=token,
        )