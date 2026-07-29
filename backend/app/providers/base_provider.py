from abc import ABC, abstractmethod
from typing import AsyncGenerator


class BaseProvider(ABC):
    """
    Abstract base class for all AI providers.
    """

    @abstractmethod
    async def generate_text(self, prompt: str) -> str:
        """
        Generate a complete text response from the given prompt.
        """
        pass

    @abstractmethod
    async def stream_text(
        self,
        prompt: str,
    ) -> AsyncGenerator[str, None]:
        """
        Stream a text response token-by-token (or chunk-by-chunk).
        """
        pass

    @abstractmethod
    async def generate_embedding(self, text: str) -> list[float]:
        """
        Generate an embedding vector for the given text.
        """
        pass