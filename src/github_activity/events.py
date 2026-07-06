from datetime import datetime
from enum import Enum


def parse_event_datetime(event: dict) -> datetime:
    return datetime.fromisoformat(event["created_at"])


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
