from __future__ import annotations

from pydantic import BaseModel


class Settings(BaseModel):
    provider: str = 'mock'
    model: str = 'mock-model'


settings = Settings()
