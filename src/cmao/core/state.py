from __future__ import annotations

from dataclasses import dataclass, field
from .types import Turn


@dataclass
class ConversationState:
    history: list[Turn] = field(default_factory=list)
    settled_points: list[str] = field(default_factory=list)
    open_threads: list[str] = field(default_factory=list)
    speaker_history: list[str] = field(default_factory=list)
    redundancy_counters: dict[str, int] = field(default_factory=dict)
