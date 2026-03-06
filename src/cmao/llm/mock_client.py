from __future__ import annotations


class MockLLMClient:
    """Deterministic-ish local mock for dev and tests."""

    def complete(self, system: str, user: str) -> str:
        # Keep this intentionally simple and predictable.
        # Useful to test orchestration + parsing without network.
        if "Return JSON" in system or "Return JSON" in user:
            return (
                '{\n'
                '  "speaker": "catalyst",\n'
                '  "objective": "Clarify the user’s intent and propose the next concrete step.",\n'
                '  "constraints": ["Be concise", "Add distinct value"],\n'
                '  "tone": "warm",\n'
                '  "avoid": ["generic agreement", "repeating the user verbatim"]\n'
                '}\n'
            )
        return "[mock] I’m here. Tell me what you want to build next, and I’ll keep it concrete."