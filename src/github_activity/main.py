import json
from urllib.request import urlopen
from urllib.error import HTTPError

import typer


app = typer.Typer()

@app.command()
def github_activity(username: str):
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

    events = json.loads(data)

    typer.echo(events)
