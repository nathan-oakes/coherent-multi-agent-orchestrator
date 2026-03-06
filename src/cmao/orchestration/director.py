from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from cmao.core.types import Directive, PersonaName
from cmao.core.state import ConversationState
from cmao.llm import get_llm_client


PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"
DIRECTOR_PROMPT_PATH = PROMPTS_DIR / "director.md"

ALLOWED_SPEAKERS: set[str] = {"anchor", "catalyst", "beacon", "scribe", "skeptic"}


def _heuristic_director(state: ConversationState) -> Directive:
    last_user = next((t.content for t in reversed(state.history) if t.role == "user"), "")
    speaker = "anchor" if any(x in last_user.lower() for x in ["sad", "angry", "anxious", "hurt", "scared"]) else "catalyst"
    return Directive(
        speaker=speaker,  # type: ignore[arg-type]
        objective="Help the user progress with clarity and coherence.",
        constraints=["Be concise", "Add distinct value"],
        tone="warm",
        avoid=["generic agreement", "repeating the user verbatim"],
    )


def _read_prompt(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    # hard fallback
    return (
        "You are the Director. Choose the best next speaker persona and produce a directive.\n\n"
        "Return JSON with:\n"
        "- speaker: one of [anchor,catalyst,beacon,scribe,skeptic]\n"
        "- objective: string\n"
        "- constraints: list of strings\n"
        "- tone: string\n"
        "- avoid: list of strings\n"
    )


def _extract_json(text: str) -> dict[str, Any]:
    """
    Accept:
      - raw JSON
      - JSON wrapped in ```json fences
      - JSON preceded/followed by commentary
    """
    s = text.strip()
    if s.startswith("```"):
        # remove code fences
        s = s.strip("`")
        # common patterns: "json\n{...}" or "{...}"
        s = s.replace("json\n", "", 1).strip()

    # Try direct parse first
    try:
        return json.loads(s)
    except Exception:
        pass

    # Try to locate first {...} block
    start = s.find("{")
    end = s.rfind("}")
    if start != -1 and end != -1 and end > start:
        return json.loads(s[start : end + 1])

    raise ValueError("No JSON object found in Director output.")


def choose_directive(state: ConversationState) -> Directive:
    llm = get_llm_client()
    system = _read_prompt(DIRECTOR_PROMPT_PATH)

    # Keep the Director input compact for v0.1.1.
    last_user = next((t.content for t in reversed(state.history) if t.role == "user"), "")
    recent = "\n".join(
        f"{t.role.upper()}: {t.content}"
        for t in state.history[-8:]
    )

    user = (
        "You are directing a multi-persona dialogue system.\n\n"
        f"Recent conversation:\n{recent}\n\n"
        f"Last user message:\n{last_user}\n\n"
        "Now return the directive JSON."
    )

    try:
        raw = llm.complete(system=system, user=user)
        data = _extract_json(raw)

        speaker = str(data.get("speaker", "")).strip().lower()
        if speaker not in ALLOWED_SPEAKERS:
            raise ValueError(f"Invalid speaker: {speaker}")

        objective = str(data.get("objective", "")).strip()
        if not objective:
            raise ValueError("Missing objective")

        constraints = data.get("constraints", [])
        avoid = data.get("avoid", [])
        tone = str(data.get("tone", "neutral")).strip()

        # Normalize lists
        if not isinstance(constraints, list):
            constraints = [str(constraints)]
        if not isinstance(avoid, list):
            avoid = [str(avoid)]

        return Directive(
            speaker=speaker,  # type: ignore[arg-type]
            objective=objective,
            constraints=[str(x) for x in constraints],
            tone=tone,
            avoid=[str(x) for x in avoid],
            meta={"raw_director": raw},
        )

    except Exception:
        # Fallback to heuristic to keep UX stable
        return _heuristic_director(state)


def directive_to_json(d: Directive) -> str:
    return json.dumps(asdict(d), indent=2)