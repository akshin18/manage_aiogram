import os
from typing import List, Union

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from aiogram.types import Message


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    DB_URL: SecretStr
    CHANNEL_ID: SecretStr
    CHAT_IDS: List
    ADMINS_ID: List
    manager_index: int = 0
    first_message: Union[Message, None] = None
    push_message: Union[Message, None] = None

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env"),
        env_file_encoding="utf-8",
    )

config = Settings()
