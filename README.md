# GitHub Activity CLI

A simple command-line tool that shows the recent public activity of a GitHub user.

This project is based on the [roadmap.sh GitHub User Activity](https://roadmap.sh/projects/github-user-activity) project idea.

## Features

- Fetch recent public GitHub activity by username
- Display activity in a readable CLI format
- Handle invalid usernames and API errors
- Use the GitHub public events API
- Built with Python and Typer

## Installation

Clone the repository:

```bash
git clone https://github.com/Curseppp/github-activity.git
cd github-activity
```
Install dependencies with uv:
```bash
uv sync
```

## Usage
Select the user whose public activity you want to view and enter their name as a command line parameter.

For example: 
```bash
uv run github-activity Curseppp
```