from __future__ import annotations

from cmao.config.settings import settings
from cmao.llm.mock_client import MockLLMClient

def get_llm_client():
    provider = (settings.provider or "mock").lower()

    if provider == "openai":
        if not settings.openai_api_key:
            # Fall back to mock if key missing
            return MockLLMClient()
        from cmao.llm.openai_client import OpenAILLMClient
        return OpenAILLMClient(api_key=settings.openai_api_key, model=settings.model)

    return MockLLMClient()