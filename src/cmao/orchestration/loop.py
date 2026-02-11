from __future__ import annotations

from cmao.core.state import ConversationState
from cmao.core.memory import add_user_turn, add_assistant_turn
from cmao.orchestration.director import choose_directive
from cmao.orchestration.speaker import run_speaker


def step(state: ConversationState, user_text: str) -> str:
    add_user_turn(state, user_text)
    directive = choose_directive(state)
    assistant_text = run_speaker(state, directive)
    add_assistant_turn(state, assistant_text)
    return assistant_text
