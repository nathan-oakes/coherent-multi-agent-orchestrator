from __future__ import annotations

from cmao.core.types import Directive
from cmao.core.state import ConversationState


def run_speaker(state: ConversationState, directive: Directive) -> str:
    # v0: placeholder. Later this will call your LLM with persona prompt + directive.
    return f"[{directive.speaker}] {directive.objective}\n(placeholder response)"
