import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import typer
from dotenv import load_dotenv

load_dotenv()


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


def fetch_user_activity(username: str) -> list[dict]:
    request = Request(
        f"https://api.github.com/users/{username}/events`",
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
