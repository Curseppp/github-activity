import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import typer
from dotenv import load_dotenv

from .events import EventType, filter_events_by_type

load_dotenv()

# GitHub Events API returns up to 300 events, with max 100 events per page.
EVENTS_PER_PAGE = 100
MAX_EVENT_PAGES = 3


def get_headers() -> dict[str, str]:
    token = os.getenv("GITHUB_TOKEN")

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10",
        "User-Agent": "github-activity-cli",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return headers

def fetch_user_activity_page(username: str, page: int = 1, per_page: int = EVENTS_PER_PAGE) -> list[dict]:
    params = urlencode({
        "per_page": per_page,
        "page": page,
    })
    request = Request(
        f"https://api.github.com/users/{username}/events?{params}",
        headers=get_headers(),
    )
    try:
        with urlopen(request, timeout=10) as response:
            data = json.loads(response.read())
    except HTTPError as err:
        if err.code == 404:
            typer.echo(f"User {username} not found")
            raise typer.Exit(code=1)

        typer.echo(f"GitHub API error: {err.code}")
        raise typer.Exit(code=1)

    return data


def fetch_user_activity(
        username: str,
        limit: int,
        event_type: EventType | None = None,
) -> list[dict]:
    if event_type is None:
        return fetch_user_activity_page(username, per_page=limit)

    events = []

    for page in range(1, MAX_EVENT_PAGES + 1):
        page_events = fetch_user_activity_page(username, page=page)

        if not page_events:
            break

        filtered_events = filter_events_by_type(page_events, event_type)
        events.extend(filtered_events)

        if len(events) >= limit:
            break

    return events[:limit]
