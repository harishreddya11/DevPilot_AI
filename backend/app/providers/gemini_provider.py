from google import genai

from app.core.config import settings
from app.providers.base_provider import BaseProvider


class GeminiProvider(BaseProvider):
    """
    Gemini implementation of the BaseProvider interface.
    """

    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.llm_model = settings.gemini_model
        self.embedding_model = settings.embedding_model

    async def generate_text(self, prompt: str) -> str:
        """
        Generate a text response using Gemini.
        """
        response = self.client.models.generate_content(
            model=self.llm_model,
            contents=prompt,
        )

        return response.text

    async def generate_embedding(self, text: str) -> list[float]:
        """
        Generate an embedding vector using Gemini.
        """
        response = self.client.models.embed_content(
            model=self.embedding_model,
            contents=text,
        )

        return response.embeddings[0].values