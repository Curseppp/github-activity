from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

from .api import fetch_user_activity
from .events import EventType, parse_event_datetime
from .formatter import format_event
from .style import gradient_text


app = typer.Typer()
console = Console()
ENV_FILE = Path(".env")
GITHUB_TOKEN_KEY = "GITHUB_TOKEN"


def save_github_token(token: str, env_file: Path = ENV_FILE) -> None:
    token = token.strip()

    if not token:
        console.print("GitHub token cannot be empty")
        raise typer.Exit(code=1)

    token_line = f"{GITHUB_TOKEN_KEY}={token}"
    lines = env_file.read_text().splitlines() if env_file.exists() else []

    for index, line in enumerate(lines):
        if line.startswith(f"{GITHUB_TOKEN_KEY}="):
            lines[index] = token_line
            break
    else:
        lines.append(token_line)

    env_file.write_text("\n".join(lines) + "\n")


def setup_github_token() -> None:
    token = typer.prompt("GitHub token", hide_input=True)
    save_github_token(token)
    console.print("GitHub token saved to .env")


@app.command()
def github_activity(
    username: str = typer.Argument(
        ...,
        help="GitHub username, or 'setup' to save a GitHub token.",
    ),
    limit: int = typer.Option(
        10,
        "--limit",
        "-l",
        min=1,
        max=100,
        help="Number of events to fetch. GitHub allows up to 100 events per page.",
    ),
    event_type: EventType | None = typer.Option(
        None,
        "--event-type",
        "-e",
        help="Filter activity by GitHub event type.",
    ),
) -> None:
    if username == "setup":
        setup_github_token()
        return

    with console.status("[bold green]Fetching GitHub activity..."):
        events = fetch_user_activity(username, limit, event_type)

        if not events:
            if event_type is None:
                console.print(f"No recent public activity found for {username}")
            else:
                console.print(f"No recent {event_type.value} activity found for {username}")
            return

        events = sorted(
            events,
            key=parse_event_datetime,
            reverse=True,
        )

        console.print(
            Align.center(
                Panel.fit(
                    gradient_text(
                        f"GitHub activity for {username}",
                        start=(180, 80, 255),
                        end=(80, 200, 255),
                    ),
                    border_style="blue",
                )
            )
        )

        if event_type is None:
            console.rule("[bold]Recent Activity[/bold]")
        else:
            console.rule(f"[bold]Recent {event_type.value}[/bold]")

        for event in events:
            console.print(format_event(event), highlight=False)

        console.print(f"Total events found: {len(events)}")
