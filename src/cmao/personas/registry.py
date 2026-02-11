from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import yaml


@dataclass(frozen=True)
class Persona:
    name: str
    description: str
    markers: list[str]


def load_persona(path: Path) -> Persona:
    data = yaml.safe_load(path.read_text(encoding='utf-8'))
    return Persona(
        name=data['name'],
        description=data['description'],
        markers=list(data.get('markers', [])),
    )
