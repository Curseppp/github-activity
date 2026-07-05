import typer

app = typer.Typer()

@app.command()
def github_activity(username: str):
    typer.echo(f"Github activity for {username}")
