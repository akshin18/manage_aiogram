import os
from typing import List, Union
from datetime import datetime

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from aiogram.types import Message
from google.oauth2.service_account import Credentials
import gspread


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    DB_URL: SecretStr
    CHANNEL_ID: SecretStr
    CHAT_IDS: List
    LAST_CHAT_ID: int
    ADMINS_ID: List
    SHEET_ID: SecretStr
    manager_index: int = 0
    first_message: Union[Message, None] = None
    push_message: Union[Message, None] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

class Google_sheet:
    def __init__(self) -> None:
        self.scope = ["https://www.googleapis.com/auth/spreadsheets"]
        self.creds = Credentials.from_service_account_file('creds.json', scopes=self.scope)
        self.client = gspread.authorize(self.creds)

        self.sheet_id = config.SHEET_ID.get_secret_value()
        self.workbook = self.client.open_by_key(self.sheet_id)

        self.sheet = self.workbook.sheet1
    
    def create_user(self, start_time, user_id, chat_id, link, bot_is_active,fm="", finish_date="", username=""):
        data = [start_time, fm, user_id, username, chat_id, link, bot_is_active, finish_date]
        self.sheet.append_row(data)

    def update_fm(self, user_id):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.sheet.update_cell(self.sheet.find(str(user_id)).row, 2, now)
    
    def update_finish(self, user_id):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.sheet.update_cell(self.sheet.find(str(user_id)).row, 8, now)

    def update_active(self, user_id):
        self.sheet.update_cell(self.sheet.find(str(user_id)).row, 7, 'false')


config = Settings()
google_sheet = Google_sheet()