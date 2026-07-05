from datetime import datetime


def format_datetime(raw_datetime: str) -> str:
    created_at = datetime.fromisoformat(raw_datetime)
    timezone_created_at = created_at.astimezone()

    return timezone_created_at.strftime(f"%Y-%m-%d %H:%M {timezone_created_at.tzname()}")


def format_event(event: dict) -> str:
    event_type = format_type(event["type"])
    repo_name = event["repo"]["name"]
    created_at = format_datetime(event["created_at"])

    return f"{event_type} by {repo_name} at {created_at}"


def format_type(type: str) -> str:
    match type:
        case "PushEvent":
            return f"[green]{type}[/green]"
        case "DeleteEvent":
            return f"[red]{type}[/red]"
        case _:
            return f"[blue]{type}[/blue]"
