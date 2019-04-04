from marshmallow import Schema, fields, post_load
from newreleases import models
from newreleases.enums import EmailNotification


class BaseSchema(Schema):
    __model__ = None

    @post_load
    def post_load(self, data):
        if self.__model__ is None:
            return data
        else:
            return self.__model__(**data)


class AuthKeySchema(BaseSchema):
    name = fields.String(required=True)
    secret = fields.String(required=True)
    authorized_networks = fields.List(fields.String())

    __model__ = models.AuthKey


class ExclusionSchema(BaseSchema):
    value = fields.String(required=True)

    __model__ = models.Exclusion


class SlackChannelSchema(BaseSchema):
    id = fields.String(required=True)
    channel = fields.String(required=True)
    team_name = fields.String(required=True)

    __model__ = models.SlackChannel


class WebhookSchema(BaseSchema):
    id = fields.String(required=True)
    name = fields.String(required=True)

    __model__ = models.Webhook


class ProjectSchema(BaseSchema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    provider = fields.String(required=True)
    url = fields.Url(required=True)
    email_notification = fields.String(default=EmailNotification.default.value)
    slack_channels = fields.Nested(SlackChannelSchema, many=True)
    hangouts_chat_webhooks = fields.List(fields.String())
    microsoft_teams_webhooks = fields.List(fields.String())
    webhooks = fields.Nested(WebhookSchema, many=True)
    exclude_version_regexp = fields.Nested(ExclusionSchema, many=True)
    exclude_prereleases = fields.Boolean(default=False)
    exclude_updated = fields.Boolean(default=False)

    __model__ = models.Project


class ReleaseSchema(BaseSchema):
    version = fields.String(required=True)
    date = fields.DateTime(required=True, fromat="%Y-%m-%dT%H:%M:%SZ")
    is_prerelease = fields.Boolean(default=False)
    is_updated = fields.Boolean(default=False)
    is_excluded = fields.Boolean(default=False)
    has_note = fields.Boolean(default=False)

    __model__ = models.Release


class ReleaseNoteSchema(BaseSchema):
    title = fields.String(default="")
    message = fields.String(default="")
    url = fields.String(default="")

    __model__ = models.ReleaseNote
