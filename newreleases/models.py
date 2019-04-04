from typing import List
from datetime import datetime
from dataclasses import dataclass, asdict, field


class ModelMeta(type):
    @property
    def fields(self):
        if hasattr(self, "Meta"):
            return self.Meta.table_fields
        return [f for f in self.__dataclass_fields__.keys() if f != "id"]

    @property
    def headers(self):
        return [field.replace("_", " ").title() for field in self.fields]


@dataclass
class ModelBase(metaclass=ModelMeta):
    def __iter__(self):
        d = asdict(self)
        return iter([d[f] for f in self.__class__.fields])


@dataclass
class AuthKey(ModelBase):
    name: str
    secret: str
    authorized_networks: List[str]


@dataclass
class Exclusion(ModelBase):
    value: str


@dataclass
class SlackChannel(ModelBase):
    id: str
    channel: str
    team_name: str


@dataclass
class Webhook(ModelBase):
    id: str
    name: str


@dataclass
class Project(ModelBase):
    id: str
    name: str
    provider: str
    url: str
    email_notification: str
    slack_channels: List[SlackChannel] = field(default_factory=list)
    hangouts_chat_webhooks: List[str] = field(default_factory=list)
    microsoft_teams_webhooks: List[str] = field(default_factory=list)
    webhooks: List[Webhook] = field(default_factory=list)
    exclude_version_regexp: List[Exclusion] = field(default_factory=list)
    exclude_prereleases: bool = False
    exclude_updated: bool = False

    class Meta:
        table_fields = ["name", "provider", "url", "email_notification"]


@dataclass
class Release(ModelBase):
    version: str
    date: datetime
    is_prerelease: bool = False
    is_updated: bool = False
    is_excluded: bool = False
    has_note: bool = False


@dataclass
class ReleaseNote(ModelBase):
    title: str = ""
    message: str = ""
    url: str = ""
