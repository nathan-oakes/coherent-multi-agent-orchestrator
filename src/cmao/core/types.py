from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

PersonaName = Literal['anchor','catalyst','beacon','scribe','skeptic']


@dataclass
class Turn:
    role: Literal['user','assistant']
    content: str


@dataclass
class Directive:
    speaker: PersonaName
    objective: str
    constraints: list[str] = field(default_factory=list)
    tone: str = 'neutral'
    avoid: list[str] = field(default_factory=list)
    meta: dict[str, Any] = field(default_factory=dict)
