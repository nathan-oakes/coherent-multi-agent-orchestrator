from __future__ import annotations

from cmao.core.types import Directive
from cmao.core.state import ConversationState


def choose_directive(state: ConversationState) -> Directive:
    # v0: trivial heuristic director. Replace with LLM director later.
    last_user = next((t.content for t in reversed(state.history) if t.role == 'user'), '')
    speaker = 'anchor' if any(x in last_user.lower() for x in ['sad','angry','anxious','hurt']) else 'catalyst'
    return Directive(
        speaker=speaker,  # type: ignore[arg-type]
        objective='Help the user progress with clarity and coherence.',
        constraints=['Be concise', 'Add distinct value'],
        tone='warm',
        avoid=['generic agreement', 'repeating user verbatim'],
    )
