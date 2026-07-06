from datetime import datetime

from rich.text import Text


def format_datetime(raw_datetime: str) -> str:
    created_at = datetime.fromisoformat(raw_datetime)
    timezone_created_at = created_at.astimezone()

    return timezone_created_at.strftime(
        f"%Y-%m-%d %H:%M {timezone_created_at.tzname()}"
    )


def format_event(event: dict) -> Text:
    event_type = event["type"]
    repo_name = event["repo"]["name"]
    created_at = format_datetime(event["created_at"])
    payload = event.get("payload", {})

    text = format_event_message(event_type, payload)
    text.append(f" in {repo_name} at {created_at}", style="white")
    return text


def format_push_event(payload) -> Text:
    text = Text()
    commits = payload.get("commits")

    if commits is None:
        text.append("↑ Pushed", style="green")
    else:
        text.append(f"↑ Pushed {len(commits)} commits", style="green")
    return text


def format_delete_event(payload) -> Text:
    text = Text()
    ref = payload.get("ref", "unknown")
    ref_type = payload.get("ref_type", "resource")
    text.append(f"✕ Deleted {ref_type} {ref}", style="red")
    return text


def format_create_event(payload) -> Text:
    text = Text()
    ref = payload.get("ref", "repository")
    ref_type = payload.get("ref_type", "repository")
    if ref:
        text.append(f"+ Created {ref_type} {ref}", style="violet")
    else:
        text.append(f"+ Created {ref_type}", style="violet")
    return text


def format_pull_request_event(payload) -> Text:
    text = Text()
    action = payload.get("action", "updated")
    pull_request = payload.get("pull_request", {})
    pr_number = payload.get("number")
    merged = pull_request.get("merged", False)

    if action == "closed" and merged:
        text.append(f"✓ Merged pull request #{pr_number}", style="purple")
    elif action == "closed":
        text.append(f"✕ Closed pull request #{pr_number}", style="red")
    elif action == "opened":
        text.append(f"+ Opened pull request #{pr_number}", style="green")
    elif action == "reopened":
        text.append(f"↻ Reopened pull request #{pr_number}", style="yellow")
    elif action == "synchronize":
        text.append(f"⟳ Updated pull request #{pr_number}", style="blue")
    else:
        text.append(f"⑂ {action.capitalize()} pull request #{pr_number}", style="cyan")

    return text


def format_pr_review_event(payload) -> Text:
    text = Text()
    pull_request = payload.get("pull_request", {})
    review = payload.get("review", {})

    pr_number = pull_request.get("number", "unknown")
    action = payload.get("action", "created")
    review_state = review.get("state", "commented")

    if action == "dismissed":
        text.append(
            f"✕ Dismissed review on pull request #{pr_number}",
            style="red",
        )
    elif review_state == "approved":
        text.append(
            f"✓ Approved pull request #{pr_number}",
            style="green",
        )
    elif review_state == "changes_requested":
        text.append(
            f"! Requested changes on pull request #{pr_number}",
            style="yellow",
        )
    elif review_state == "commented":
        text.append(
            f"✎ Reviewed pull request #{pr_number}",
            style="blue",
        )
    else:
        text.append(
            f"◌ {action.capitalize()} review on pull request #{pr_number}",
            style="cyan",
        )
    return text


def format_pr_review_comment_event(payload) -> Text:
    text = Text()
    pull_request = payload.get("pull_request", {})
    comment = payload.get("comment", {})

    action = payload.get("action", "created")
    pr_number = pull_request.get("number", "unknown")
    path = comment.get("path", "unknown file")

    match action:
        case "created":
            text.append(
                f"✎ Commented on pull request #{pr_number} in {path}",
                style="magenta",
            )
        case _:
            text.append(
                f"✎ {action.capitalize()} review comment on pull request #{pr_number} in {path}",
                style="magenta",
            )
    return text


def format_watch_event(payload) -> Text:
    text = Text()
    action = payload.get("action", "started")

    if action == "started":
        text.append(
            "☆ Starred repository",
            style="yellow",
        )
    return text


def format_issue_comment_event(payload) -> Text:
    text = Text()
    action = payload.get("action", "unknown")
    issue = payload.get("issue", {})

    issue_number = issue.get("number", "unknown")
    is_pr = "pull_request" in issue

    target = "pull request" if is_pr else "issue"

    match action:
        case "created":
            text.append(
                f"✎ Commented on {target} #{issue_number}",
                style="blue",
            )
        case "edited":
            text.append(
                f"✎ Edited comment on {target} #{issue_number}",
                style="yellow",
            )
        case "deleted":
            text.append(
                f"✕ Deleted comment on {target} #{issue_number}",
                style="red",
            )
        case _:
            text.append(
                f"✎ {action.capitalize()} comment on {target} #{issue_number}",
                style="cyan",
            )
    return text


def format_issues_event(payload) -> Text:
    text = Text()
    action = payload.get("action", "unknown")
    issue = payload.get("issue", {})

    issue_number = issue.get("number", "unknown")

    match action:
        case "opened":
            text.append(
                f"+ Opened issue #{issue_number}",
                style="green",
            )
        case "closed":
            text.append(
                f"✓ Closed issue #{issue_number}",
                style="red",
            )
        case "reopened":
            text.append(
                f"↻ Reopened issue #{issue_number}",
                style="yellow",
            )
        case "assigned":
            assignee = payload.get("assignee", {})
            assignee_login = assignee.get("login", "someone")

            text.append(
                f"@ Assigned {assignee_login} to issue #{issue_number}",
                style="blue",
            )
        case "unassigned":
            assignee = payload.get("assignee", {})
            assignee_login = assignee.get("login", "someone")

            text.append(
                f"@ Unassigned {assignee_login} from issue #{issue_number}",
                style="blue",
            )
        case "labeled":
            label = payload.get("label", {})
            label_name = label.get("name", "unknown label")

            text.append(
                f"# Added label {label_name} to issue #{issue_number}",
                style="magenta",
            )
        case "unlabeled":
            label = payload.get("label", {})
            label_name = label.get("name", "unknown label")

            text.append(
                f"# Removed label {label_name} from issue #{issue_number}",
                style="magenta",
            )
        case _:
            text.append(
                f"● {action.capitalize()} issue #{issue_number}",
                style="cyan",
            )
    return text


def format_event_message(event_type: str, payload: dict) -> Text:
    match event_type:
        case "PushEvent":
            return format_push_event(payload)
        case "DeleteEvent":
            return format_delete_event(payload)
        case "CreateEvent":
            return format_create_event(payload)
        case "PullRequestEvent":
            return format_pull_request_event(payload)
        case "PullRequestReviewEvent":
            return format_pr_review_event(payload)
        case "PullRequestReviewCommentEvent":
            return format_pr_review_comment_event(payload)
        case "IssuesEvent":
            return format_issues_event(payload)
        case "IssueCommentEvent":
            return format_issue_comment_event(payload)
        case "WatchEvent":
            return format_watch_event(payload)

        case _:
            return Text(event_type)
