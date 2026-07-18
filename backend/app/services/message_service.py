import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.chat import Chat
from app.models.message import Message
from app.models.user import User
from app.schemas.message import (
    ChatConversationResponse,
    MessageCreate,
)
from app.services.assistant_service import AssistantService


class MessageService:
    def __init__(self, db: Session):
        self.db = db
        self.assistant_service = AssistantService()

    def _get_chat(
        self,
        chat_id: uuid.UUID,
        current_user: User,
    ) -> Chat:
        chat = (
            self.db.query(Chat)
            .filter(
                Chat.id == chat_id,
                Chat.user_id == current_user.id,
            )
            .first()
        )

        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )

        return chat

    def _save_message(
        self,
        chat_id: uuid.UUID,
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

    def _build_conversation(
        self,
        chat_id: uuid.UUID,
    ) -> list[dict]:
        messages = (
            self.db.query(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(Message.created_at.asc())
            .all()
        )

        conversation = [
            {
                "role": "system",
                "content": (
                    "You are DevPilot AI, a helpful software engineering assistant."
                ),
            }
        ]

        for message in messages:
            conversation.append(
                {
                    "role": message.role,
                    "content": message.content,
                }
            )

        return conversation

    def send_message(
        self,
        chat_id: uuid.UUID,
        message_data: MessageCreate,
        current_user: User,
    ) -> ChatConversationResponse:
        # Verify the chat belongs to the current user
        self._get_chat(chat_id, current_user)

        # Save the user's message
        user_message = self._save_message(
            chat_id=chat_id,
            role="user",
            content=message_data.content,
        )

        # Build the conversation history
        conversation_history = self._build_conversation(chat_id)

        # Generate AI response
        ai_text = self.assistant_service.generate_response(
            conversation_history
        )

        # Save the assistant's response
        assistant_message = self._save_message(
            chat_id=chat_id,
            role="assistant",
            content=ai_text,
        )

        return ChatConversationResponse(
            user_message=user_message,
            assistant_message=assistant_message,
        )