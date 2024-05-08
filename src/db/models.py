from tortoise import fields
from tortoise.models import Model
import pytz
import datetime


class User(Model):
    id = fields.BigIntField(pk=True)
    user_id = fields.BigIntField(null=False, unique=True)
    topic_id = fields.IntField(null=True)
    chat_id = fields.IntField(null=False)
    
    name = fields.CharField(max_length=50, null=True)
    reg_id = fields.CharField(max_length=100, null=True)
    username = fields.CharField(max_length=32, null=True)
    state = fields.IntField(null=False, default=0)
    invite_link = fields.CharField(max_length=100, null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)