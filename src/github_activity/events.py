from datetime import datetime
from enum import Enum


class EventType(str, Enum):
    PUSH = "PushEvent"
    DELETE = "DeleteEvent"
    CREATE = "CreateEvent"
    PULL_REQUEST = "PullRequestEvent"
    PULL_REQUEST_REVIEW = "PullRequestReviewEvent"
    PULL_REQUEST_REVIEW_COMMENT = "PullRequestReviewCommentEvent"
    ISSUES = "IssuesEvent"
    ISSUE_COMMENT = "IssueCommentEvent"
    WATCH = "WatchEvent"


def parse_event_datetime(event: dict) -> datetime:
    return datetime.fromisoformat(event["created_at"])


def filter_events_by_type(events: list[dict], event_type: EventType | None) -> list[dict]:
    if event_type is None:
        return events

    return [event for event in events if event["type"] == event_type]

