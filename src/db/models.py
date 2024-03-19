from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=50, null=True)
    username = fields.CharField(max_length=32, null=True)