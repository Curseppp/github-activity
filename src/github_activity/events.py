from datetime import datetime


def parse_event_datetime(event: dict) -> datetime:
    return datetime.fromisoformat(event["created_at"])
