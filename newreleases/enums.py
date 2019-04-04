import enum


class EnumMeta(enum.EnumMeta):
    @property
    def choices(cls):
        return cls.__members__

    def click_callback(cls, context, option, value):
        return getattr(cls, value) if value else None


class Enum(enum.Enum, metaclass=EnumMeta):
    pass


class Provider(Enum):
    github = "github"
    gitlab = "gitlab"
    bitbucket = "bitbucket"
    pypi = "pypi"
    maven = "maven"
    npm = "npm"
    yarn = "yarn"
    gems = "gems"
    packagist = "packagist"
    dockerhub = "dockerhub"


class SortOrder(Enum):
    name = "name"
    updated = "updated"
    added = "added"


class EmailNotification(Enum):
    none = "none"
    hourly = "hourly"
    daily = "daily"
    weekly = "weekly"
    default = "default"
