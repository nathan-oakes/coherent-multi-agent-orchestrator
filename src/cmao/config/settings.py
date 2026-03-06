from __future__ import annotations

from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    # LLM provider selection: "mock" | "openai"
    provider: str = os.getenv("CMAO_PROVIDER", "mock")
    model: str = os.getenv("CMAO_MODEL", "gpt-4o-mini")

    # OpenAI
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")


settings = Settings()