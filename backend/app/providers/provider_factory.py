"""
Provider Factory

Returns the configured LLM provider instance.

Supported providers:
- Gemini
- OpenAI (future)
- OpenRouter (future)
"""

from app.core.config import settings
from app.providers.base_provider import BaseProvider
from app.providers.gemini_provider import GeminiProvider


class ProviderFactory:
    """Factory class for creating provider instances."""

    @staticmethod
    def get_provider() -> BaseProvider:
        provider = settings.llm_provider.lower()

        providers = {
            "gemini": GeminiProvider,
            # "openai": OpenAIProvider,
            # "openrouter": OpenRouterProvider,
        }

        provider_class = providers.get(provider)

        if provider_class is None:
            supported = ", ".join(providers.keys())
            raise ValueError(
                f"Unsupported provider: '{provider}'. "
                f"Supported providers: {supported}"
            )

        return provider_class()