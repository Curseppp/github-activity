import typer
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

from .api import fetch_user_activity
from .events import parse_event_datetime
from .formatter import format_event
from .style import gradient_text


app = typer.Typer()
console = Console()


@app.command()
def github_activity(
    username: str,
    limit: int = typer.Option(
        10,
        "--limit",
        "-l",
        min=1,
        max=100,
        help="Number of events to fetch. GitHub allows up to 100 events per page.",
    ),
) -> None:
    with console.status("[bold green]Fetching GitHub activity..."):
        events = fetch_user_activity(username, limit)

        if not events:
            console.print(f"No recent public activity found for {username}")
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

        console.rule("[bold]Recent Activity[/bold]")

        for event in events:
            console.print(format_event(event), highlight=False)
