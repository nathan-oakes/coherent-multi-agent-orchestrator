from __future__ import annotations

from typing import Optional

try:
    from openai import OpenAI
except Exception as e:  # pragma: no cover
    OpenAI = None  # type: ignore[assignment]


class OpenAILLMClient:
    def __init__(self, api_key: str, model: str) -> None:
        if OpenAI is None:
            raise RuntimeError(
                "OpenAI SDK not installed. Run: pip install openai\n"
                "Or set CMAO_PROVIDER=mock to use the mock client."
            )
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def complete(self, system: str, user: str) -> str:
        resp = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.6,
        )
        return resp.choices[0].message.content or ""