from abc import ABC, abstractmethod

from app.schemas.assistant import AssistantRequest, AssistantResponse


class BaseLLMProvider(ABC):
    """
    Base interface for all LLM providers.
    """

    @abstractmethod
    def generate_response(
        self,
        request: AssistantRequest,
    ) -> AssistantResponse:
        """
        Generate a response from the language model.
        """
        pass