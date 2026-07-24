from app.db.base import Base

# Import all models so Alembic can discover them
from app.models.user import User
from app.models.chat import Chat
from app.models.message import Message
from app.models.document import Document
from app.models.project import Project
from app.models.document import Document