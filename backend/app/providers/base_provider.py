from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """
    Abstract base class for all AI providers.
    """

    @abstractmethod
    async def generate_text(self, prompt: str) -> str:
        """
        Generate a text response from the given prompt.
        """
        pass

    @abstractmethod
    async def generate_embedding(self, text: str) -> list[float]:
        """
        Generate an embedding vector for the given text.
        """
        pass