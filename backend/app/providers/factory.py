from app.core.config import get_settings
from app.providers.gemini import GeminiProvider
from app.providers.openrouter import OpenRouterProvider


class ProviderFactory:

    @staticmethod
    def get_provider():
        settings = get_settings()

        provider = settings.llm_provider.lower()

        if provider == "gemini":
            return GeminiProvider()

        if provider == "openrouter":
            return OpenRouterProvider()

        raise ValueError(
            f"Unsupported provider: {provider}"
        )