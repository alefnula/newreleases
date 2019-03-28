from marshmallow import Schema, fields, post_load
from newreleases import models


class BaseSchema(Schema):
    __model__ = None

    @post_load
    def post_load(self, data):
        if self.__model__ is None:
            return data
        else:
            return self.__model__(**data)


class ProjectSchema(BaseSchema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    provider = fields.String(required=True)
    url = fields.Url(required=True)
    email_notification = fields.String(required=True)

    __model__ = models.Project
