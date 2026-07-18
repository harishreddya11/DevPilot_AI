import httpx

from app.core.config import get_settings


class OpenRouterClient:

    def __init__(self):

        settings = get_settings()

        self.base_url = settings.openrouter_base_url
        self.api_key = settings.openrouter_api_key

        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=60,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )

    def post(
        self,
        endpoint: str,
        payload: dict,
    ):

        response = self.client.post(
            endpoint,
            json=payload,
        )

        response.raise_for_status()

        return response.json()