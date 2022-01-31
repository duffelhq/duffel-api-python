from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Sequence


@dataclass
class Webhook:
    """
    Webhooks are used to automatically receive notifications of events that
    happen. For example, when an order has a schedule change.
    """

    id: str
    live_mode: bool
    active: bool
    created_at: datetime
    events: Sequence[str]
    updated_at: datetime
    url: str
    secret: Optional[str]

    @classmethod
    def from_json(cls, json: dict):
        """Construct a class instance from a JSON response."""
        return cls(
            id=json["id"],
            live_mode=json["live_mode"],
            active=json["active"],
            created_at=datetime.strptime(json["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            events=json["events"],
            updated_at=datetime.strptime(json["updated_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            url=json["url"],
            secret=json.get("secret"),
        )
