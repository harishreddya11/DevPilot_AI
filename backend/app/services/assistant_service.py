from uuid import UUID

from sqlalchemy.orm import Session

from app.providers.provider_factory import ProviderFactory
from app.services.chat_service import ChatService
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


class AssistantService:
    """
    Retrieval-Augmented Generation (RAG) Assistant Service.

    Responsibilities:
    - Validate chat ownership
    - Save user message
    - Retrieve conversation history
    - Retrieve relevant document chunks
    - Generate AI response
    - Save assistant response
    """

    def __init__(self, db: Session):
        self.provider = ProviderFactory.get_provider()

        self.chat_service = ChatService(db)

        self.vector_service = VectorService(
            db=db,
            embedding_service=EmbeddingService(),
        )

    async def ask(
        self,
        *,
        user_id: UUID,
        chat_id: UUID,
        question: str,
    ) -> str:
        """
        Answer a user's question using RAG while maintaining
        conversation history.
        """

        # Validate chat
        chat = self.chat_service.get_chat(
            chat_id=chat_id,
            user_id=user_id,
        )

        if chat is None:
            raise ValueError("Chat not found.")

        # Save current user message
        self.chat_service.save_user_message(
            chat_id=chat_id,
            content=question,
        )

        # Load recent conversation
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

            conversation += (
                f"{role}: {message.content}\n"
            )

        # Retrieve relevant document chunks
        context_chunks = await self.vector_service.search(
            user_id=user_id,
            query=question,
            top_k=5,
        )

        context = (
            "\n\n".join(context_chunks)
            if context_chunks
            else "No relevant context found."
        )

        prompt = f"""
You are DevPilot AI, an intelligent document assistant.

Your job is to answer the user's question using:

1. Previous conversation
2. Retrieved document context

Rules:
- Prefer information from the retrieved context.
- Use previous conversation only to understand follow-up questions.
- If the answer is not available in the context, respond exactly with:

"I couldn't find that information in the uploaded documents."

----------------------------
Conversation History
----------------------------
{conversation}

----------------------------
Retrieved Context
----------------------------
{context}

----------------------------
Current Question
----------------------------
{question}

----------------------------
Answer
----------------------------
"""

        answer = await self.provider.generate_text(prompt)

        answer = answer.strip()

        # Save assistant response
        self.chat_service.save_ai_message(
            chat_id=chat_id,
            content=answer,
        )

        return answer