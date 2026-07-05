from datetime import datetime

import typer
from rich.console import Console

from .api import fetch_user_activity
from .formatter import format_event
from .style import gradient_text


app = typer.Typer()
console = Console()


@app.command()
def github_activity(username: str) -> None:
    events = fetch_user_activity(username)

    if not events:
        console.print(f"No recent public activity found for {username}")
        return

    events = sorted(
        events,
        key=lambda event: datetime.fromisoformat(event["created_at"]),
        reverse=True,
    )

    console.print(
        gradient_text(
            f"GitHub activity for {username}",
            start=(180, 80, 255),
            end=(80, 200, 255),
        ),
        justify="center",
    )

    for event in events:
        console.print(format_event(event), highlight=False)
