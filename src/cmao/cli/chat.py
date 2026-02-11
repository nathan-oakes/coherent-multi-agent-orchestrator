from __future__ import annotations

from rich.console import Console

from cmao.core.state import ConversationState
from cmao.orchestration.loop import step


def main() -> None:
    console = Console()
    state = ConversationState()
    console.print('[bold]CMAO[/bold] (v0.1) — type \'exit\' to quit.')
    while True:
        user = console.input('\n[bold cyan]You[/bold cyan]: ').strip()
        if user.lower() in {'exit', 'quit'}:
            break
        resp = step(state, user)
        console.print(f'[bold green]CMAO[/bold green]: {resp}')
