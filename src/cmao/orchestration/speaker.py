from __future__ import annotations

from pathlib import Path

import yaml

from cmao.core.types import Directive
from cmao.core.state import ConversationState
from cmao.llm import get_llm_client


BASE_DIR = Path(__file__).resolve().parents[1]
PERSONAS_DIR = BASE_DIR / "personas"
PROMPTS_DIR = BASE_DIR / "prompts"
SPEAKER_PROMPT_PATH = PROMPTS_DIR / "speaker.md"


def _read_text(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def _load_persona_yaml(name: str) -> dict:
    path = PERSONAS_DIR / f"{name}.yaml"
    if not path.exists():
        return {"name": name, "description": "", "markers": []}
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def run_speaker(state: ConversationState, directive: Directive) -> str:
    llm = get_llm_client()

    persona = _load_persona_yaml(directive.speaker)
    persona_name = persona.get("name", directive.speaker)
    persona_desc = persona.get("description", "")
    markers = persona.get("markers", []) or []

    system = _read_text(SPEAKER_PROMPT_PATH).strip()
    if not system:
        system = (
            "You are a persona speaker. Follow the Director's directive.\n"
            "- Add distinct contribution (no empty agreement).\n"
            "- Reference specifics.\n"
            "- Avoid repeating settled points unless justified.\n"
        )

    recent = "\n".join(
        f"{t.role.upper()}: {t.content}"
        for t in state.history[-10:]
    )

    user = (
        f"Persona: {persona_name}\n"
        f"Persona description: {persona_desc}\n"
        f"Persona markers: {markers}\n\n"
        f"Director objective: {directive.objective}\n"
        f"Constraints: {directive.constraints}\n"
        f"Tone: {directive.tone}\n"
        f"Avoid: {directive.avoid}\n\n"
        f"Recent conversation:\n{recent}\n\n"
        "Write the next assistant response now."
    )

    try:
        return llm.complete(system=system, user=user).strip()
    except Exception as e:
        return f"[{directive.speaker}] (LLM error) {e}"