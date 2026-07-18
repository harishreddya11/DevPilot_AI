from app.core.config import get_settings
from app.llm.dummy_provider import DummyProvider
from app.llm.openrouter_provider import OpenRouterProvider
from app.llm.base import BaseLLMProvider


class ProviderFactory:

    @staticmethod
    def get_provider() -> BaseLLMProvider:

        settings = get_settings()

        provider = settings.llm_provider.lower()

        if provider == "openrouter":
            return OpenRouterProvider()

        return DummyProvider()