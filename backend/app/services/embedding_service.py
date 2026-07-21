from app.providers.provider_factory import ProviderFactory


class EmbeddingService:
    """
    Service responsible for generating vector embeddings.
    """

    def __init__(self):
        self.provider = ProviderFactory.get_provider()

    async def generate_embedding(self, text: str) -> list[float]:
        """
        Generate an embedding for a single piece of text.
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        return await self.provider.generate_embedding(text)

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple text chunks.
        """

        if not texts:
            return []

        embeddings = []

        for text in texts:
            embedding = await self.generate_embedding(text)
            embeddings.append(embedding)

        return embeddings