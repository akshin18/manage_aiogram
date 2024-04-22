import os
from typing import List, Union
from datetime import datetime

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from aiogram.types import Message
from google.oauth2.service_account import Credentials
import gspread
from gspread.cell import Cell
from loguru import logger
import pytz


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    DB_URL: SecretStr
    CHANNEL_ID: SecretStr
    CHAT_IDS: List
    LAST_CHAT_ID: int
    ADMINS_ID: List
    SHEET_ID: SecretStr
    manager_index: int = 0
    first_message: Union[Message, str ,None]
    push_message: Union[Message, str, None]
    time_to_push: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


class Google_sheet:
    def __init__(self) -> None:
        self.scope = ["https://www.googleapis.com/auth/spreadsheets"]
        self.creds = Credentials.from_service_account_file(
            "creds.json", scopes=self.scope
        )
        self.client = gspread.authorize(self.creds)

        self.sheet_id = config.SHEET_ID.get_secret_value()
        self.workbook = self.client.open_by_key(self.sheet_id)

        self.sheet = self.workbook.sheet1
        self.moscow_timezone = pytz.timezone('Europe/Moscow')

    def create_user(
        self,
        start_date,
        start_time,
        user_id,
        chat_id,
        link,
        bot_is_active,
        fm_date="",
        fm_time="",
        finish_date="",
        finish_time="",
        username="",
    ):
        data = [
            start_date,
            start_time,
            fm_date,
            fm_time,
            user_id,
            username,
            chat_id,
            link,
            bot_is_active,
            finish_date,
            finish_time,
        ]
        self.sheet.append_row(data,table_range="A1")

    def update_fm(self, user_id):
        now = datetime.now(self.moscow_timezone)
        try:
            # self.sheet.update_cell(self.sheet.find(str(user_id)).row, 2, now)
            self.sheet.update_cells(
                [
                    Cell(self.sheet.find(str(user_id)).row, 3, now.strftime("%d/%m/%Y")),
                    Cell(self.sheet.find(str(user_id)).row, 4, now.strftime("%H:%M")),
                ]
            )
        except Exception as e:
            logger.error(f"update error {e}")

    def update_finish(self, user_id):
        now = datetime.now(self.moscow_timezone)
        try:
            # self.sheet.update_cell(self.sheet.find(str(user_id)).row, 8, now)
            self.sheet.update_cells(
                [
                    Cell(self.sheet.find(str(user_id)).row, 10, now.strftime("%d/%m/%Y")),
                    Cell(self.sheet.find(str(user_id)).row, 11, now.strftime("%H:%M")),
                ]
            )
        except Exception as e:
            logger.error(f"update error {e}")

    def update_active(self, user_id):
        try:
            self.sheet.update_cell(self.sheet.find(str(user_id)).row, 9, "FALSE")
        except Exception as e:
            logger.error(f"update error {e}")

    def reg(self, user_id):
        now = datetime.now(self.moscow_timezone)
        try:
            self.sheet.update_cells(
                [
                    Cell(self.sheet.find(str(user_id)).row, 12, "yes"),
                    Cell(self.sheet.find(str(user_id)).row, 13, now.strftime("%d/%m/%Y")),
                    Cell(self.sheet.find(str(user_id)).row, 14, now.strftime("%H:%M")),
                ]
            )
        except Exception as e:
            logger.error(f"update error {e}")

    def dep(self, user_id):
        now = datetime.now(self.moscow_timezone)
        try:
            self.sheet.update_cells(
                [
                    Cell(self.sheet.find(str(user_id)).row, 15, "yes"),
                    Cell(self.sheet.find(str(user_id)).row, 16, now.strftime("%d/%m/%Y")),
                    Cell(self.sheet.find(str(user_id)).row, 17, now.strftime("%H:%M")),
                ]
            )
        except Exception as e:
            logger.error(f"update error {e}")

    def auto(self, user_id):
        try:
            self.sheet.update_cell(self.sheet.find(str(user_id)).row, 18, "auto")
        except Exception as e:
            logger.error(f"update error {e}")


config = Settings()
logger.warning(config.first_message)
google_sheet = Google_sheet()
os.environ['TZ'] = 'Europe/Moscow'
