from __future__ import annotations

from .state import ConversationState
from .types import Turn


def add_user_turn(state: ConversationState, text: str) -> None:
    state.history.append(Turn(role='user', content=text))


def add_assistant_turn(state: ConversationState, text: str) -> None:
    state.history.append(Turn(role='assistant', content=text))
