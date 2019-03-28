from dataclasses import dataclass


@dataclass
class Project:
    id: str
    name: str
    provider: str
    url: str
    email_notification: str
