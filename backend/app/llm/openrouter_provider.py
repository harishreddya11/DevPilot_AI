from app.core.config import get_settings
from app.llm.base import BaseLLMProvider
from app.llm.client import OpenRouterClient
from app.llm.prompt_builder import PromptBuilder
from app.schemas.assistant import (
    AssistantRequest,
    AssistantResponse,
)


class OpenRouterProvider(BaseLLMProvider):

    def __init__(self):
        self.settings = get_settings()
        self.client = OpenRouterClient()

    def generate_response(
        self,
        request: AssistantRequest,
    ) -> AssistantResponse:

        prompt = PromptBuilder.build(request)

        payload = {
            "model": self.settings.openrouter_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }

        result = self.client.post(
            "/chat/completions",
            payload,
        )

        message = result["choices"][0]["message"]["content"]

        return AssistantResponse(
            response=message,
            model=self.settings.openrouter_model,
        )