from aiogram.filters import BaseFilter
from aiogram.types import Message

from config_reader import config


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id in config.ADMINS_ID:
            return True