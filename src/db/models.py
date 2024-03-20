from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField(null=False, unique=True)
    topic_id = fields.IntField(null=True)
    
    name = fields.CharField(max_length=50, null=True)
    username = fields.CharField(max_length=32, null=True)
    manager_index = fields.IntField(null=False)
    state = fields.IntField(null=False, default=0)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)