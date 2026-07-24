from uuid import UUID

from sqlalchemy.orm import Session

from app.models.chat import Chat
from app.models.message import Message
from app.repositories.chat_repository import ChatRepository
from app.repositories.message_repository import MessageRepository


class ChatService:
    def __init__(self, db: Session):
        self.chat_repository = ChatRepository(db)
        self.message_repository = MessageRepository(db)

    def create_chat(
        self,
        *,
        title: str,
        user_id: UUID,
        project_id: UUID,
    ) -> Chat:
        """
        Create a new chat.
        """
        return self.chat_repository.create(
            title=title,
            user_id=user_id,
        )

    def get_chat(
        self,
        *,
        chat_id: UUID,
        user_id: UUID,
    ) -> Chat | None:
        """
        Get a user's chat.
        """
        return self.chat_repository.get_user_chat(
            chat_id=chat_id,
            user_id=user_id,
        )

    def list_chats(
        self,
        *,
        user_id: UUID,
    ) -> list[Chat]:
        """
        List all chats for a user.
        """
        return self.chat_repository.list_by_user(user_id)

    def save_user_message(
        self,
        *,
        chat_id: UUID,
        content: str,
    ) -> Message:
        """
        Save a user message.
        """
        return self.message_repository.create(
            chat_id=chat_id,
            role="user",
            content=content,
        )

    def save_ai_message(
        self,
        *,
        chat_id: UUID,
        content: str,
    ) -> Message:
        """
        Save an AI message.
        """
        return self.message_repository.create(
            chat_id=chat_id,
            role="assistant",
            content=content,
        )

    def get_chat_history(
        self,
        *,
        chat_id: UUID,
    ) -> list[Message]:
        """
        Get all messages in a chat.
        """
        return self.message_repository.list_by_chat(chat_id)

    def delete_chat(
        self,
        *,
        chat_id: UUID,
        user_id: UUID,
    ) -> bool:
        """
        Delete a chat and all its messages.
        """
        chat = self.chat_repository.get_user_chat(
            chat_id=chat_id,
            user_id=user_id,
        )

        if chat is None:
            return False

        self.message_repository.delete_by_chat(chat_id)
        self.chat_repository.delete(chat)

        return True
    
    def get_recent_messages(
        self,
        *,
        chat_id: UUID,
        limit: int = 10,
    ):
        return self.message_repository.get_recent_messages(
            chat_id=chat_id,
            limit=limit,
        )