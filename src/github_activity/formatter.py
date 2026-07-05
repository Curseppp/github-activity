from datetime import datetime


def format_datetime(raw_datetime: str) -> str:
    created_at = datetime.fromisoformat(raw_datetime)
    timezone_created_at = created_at.astimezone()

    return timezone_created_at.strftime(
        f"%Y-%m-%d %H:%M {timezone_created_at.tzname()}"
    )


def format_event(event: dict) -> str:
    event_type = event["type"]
    repo_name = event["repo"]["name"]
    created_at = format_datetime(event["created_at"])
    main_text = ""

    if event_type == "PushEvent":
        commits = event["payload"].get("commits")

        if commits is None:
            main_text = f"\nPushed 1 commit to {repo_name}"
        else:
            main_text = f"\nPushed {len(commits)} commit(s) to {repo_name}"

    return f"{format_type(event_type)} by {repo_name} at {created_at}{main_text}"


def format_type(type: str) -> str:
    match type:
        case "PushEvent":
            return f"[green]{type}[/green]"
        case "DeleteEvent":
            return f"[red]{type}[/red]"
        case _:
            return f"[blue]{type}[/blue]"
