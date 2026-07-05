import json
from urllib.request import urlopen
from urllib.error import HTTPError

import typer


def fetch_user_activity(username: str) -> list[dict]:
    url = f"https://api.github.com/users/{username}/events"

    try:
        with urlopen(url) as response:
            data = response.read()
    except HTTPError as err:
        if err.code == 404:
            typer.echo(f"User {username} not found")
            raise typer.Exit(code=1)

        typer.echo(f"GitHub API error: {err.code}")
        raise typer.Exit(code=1)

    return json.loads(data)
