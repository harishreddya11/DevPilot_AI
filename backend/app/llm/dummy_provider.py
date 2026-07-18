from app.llm.base import BaseLLMProvider
from app.schemas.assistant import (
    AssistantRequest,
    AssistantResponse,
)


class DummyProvider(BaseLLMProvider):
    """
    Dummy provider used during development
    before integrating a real LLM.
    """

    def generate_response(
        self,
        request: AssistantRequest,
    ) -> AssistantResponse:

        return AssistantResponse(
            response=f"You said: {request.prompt}",
            model="dummy-provider",
        )