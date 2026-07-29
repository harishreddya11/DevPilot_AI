from typing import AsyncGenerator
from uuid import UUID

from sqlalchemy.orm import Session

from app.providers.provider_factory import ProviderFactory
from app.repositories.document_repository import DocumentRepository
from app.services.chat_service import ChatService
from app.services.vector_service import VectorService


class AssistantService:
    """
    Retrieval-Augmented Generation (RAG) Assistant Service.

    Responsibilities:
    - Validate chat ownership
    - Save user messages
    - Retrieve conversation history
    - Retrieve relevant document chunks
    - Generate AI responses
    - Save assistant responses
    """

    def __init__(self, db: Session):
        self.provider = ProviderFactory.get_provider()

        self.chat_service = ChatService(db)

        self.document_repository = DocumentRepository(db)

        self.vector_service = VectorService(
            document_repository=self.document_repository
        )

    def _build_prompt(
        self,
        *,
        conversation: str,
        context: str,
        question: str,
    ) -> str:
        """
        Build the RAG prompt.
        """

        return f"""
You are DevPilot AI, an intelligent document assistant.

Your job is to answer the user's question using:

1. Previous conversation
2. Retrieved document context

Rules:
- Prefer information from the retrieved context.
- Use previous conversation only for follow-up questions.
- Do not make up information.
- If the answer is unavailable in the retrieved context, reply exactly:

"I couldn't find that information in the uploaded documents."

--------------------------------
Conversation History
--------------------------------
{conversation}

--------------------------------
Retrieved Context
--------------------------------
{context}

--------------------------------
Current Question
--------------------------------
{question}

--------------------------------
Answer
--------------------------------
"""

    async def ask(
        self,
        *,
        user_id: UUID,
        chat_id: UUID,
        question: str,
    ) -> dict:
        """
        Generate a complete AI response.
        """

        # Validate chat ownership
        chat = self.chat_service.get_chat(
            chat_id=chat_id,
            user_id=user_id,
        )

        if chat is None:
            raise ValueError("Chat not found.")

        # Save user message
        self.chat_service.save_user_message(
            chat_id=chat_id,
            content=question,
        )

        # Conversation history
        history = self.chat_service.get_recent_messages(
            chat_id=chat_id,
            limit=10,
        )

        conversation = ""

        for message in history:
            role = (
                "User"
                if message.role == "user"
                else "Assistant"
            )

            conversation += f"{role}: {message.content}\n"

        # Semantic Search
        context_chunks = self.vector_service.search(
            project_id=chat.project_id,
            query=question,
            top_k=5,
        )

        if context_chunks:
            context = "\n\n".join(
                chunk.content
                for chunk in context_chunks
            )
        else:
            context = "No relevant context found."

        prompt = self._build_prompt(
            conversation=conversation,
            context=context,
            question=question,
        )

        answer = await self.provider.generate_text(prompt)

        answer = answer.strip()

        # Save assistant message
        self.chat_service.save_ai_message(
            chat_id=chat_id,
            content=answer,
        )

        # Build citations
        sources = [
            {
                "document": chunk.document.filename,
                "chunk_index": chunk.chunk_index,
            }
            for chunk in context_chunks
        ]

        return {
            "answer": answer,
            "sources": sources,
        }

    async def stream_chat(
        self,
        *,
        user_id: UUID,
        chat_id: UUID,
        question: str,
    ) -> AsyncGenerator[str, None]:
        """
        Stream the AI response token-by-token.
        """

        # Validate chat ownership
        chat = self.chat_service.get_chat(
            chat_id=chat_id,
            user_id=user_id,
        )

        if chat is None:
            raise ValueError("Chat not found.")

        # Save user message
        self.chat_service.save_user_message(
            chat_id=chat_id,
            content=question,
        )

        # Conversation history
        history = self.chat_service.get_recent_messages(
            chat_id=chat_id,
            limit=10,
        )

        conversation = ""

        for message in history:
            role = (
                "User"
                if message.role == "user"
                else "Assistant"
            )

            conversation += f"{role}: {message.content}\n"

        # Semantic Search
        context_chunks = self.vector_service.search(
            project_id=chat.project_id,
            query=question,
            top_k=5,
        )

        if context_chunks:
            context = "\n\n".join(
                chunk.content
                for chunk in context_chunks
            )
        else:
            context = "No relevant context found."

        prompt = self._build_prompt(
            conversation=conversation,
            context=context,
            question=question,
        )

        complete_answer = ""

        async for chunk in self.provider.stream_text(prompt):
            complete_answer += chunk
            yield chunk

        complete_answer = complete_answer.strip()

        # Save final AI message
        self.chat_service.save_ai_message(
            chat_id=chat_id,
            content=complete_answer,
        )