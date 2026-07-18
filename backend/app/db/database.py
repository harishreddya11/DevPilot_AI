from sqlalchemy import create_engine

from app.core.config import get_settings

settings = get_settings()

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.postgres_user}:"
    f"{settings.postgres_password}@"
    f"{settings.postgres_host}:"
    f"{settings.postgres_port}/"
    f"{settings.postgres_db}"
)

engine = create_engine(
    DATABASE_URL,
    echo=settings.debug,
    pool_pre_ping=True,
)