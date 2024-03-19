import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, ChatJoinRequest
from tortoise import Tortoise

from config_reader import config


bot = Bot(config.BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.chat_join_request(F.chat.id == int(config.CHANNEL_ID.get_secret_value()))
async def chat_join_handler(request: ChatJoinRequest):
    user_id = request.from_user.id
    await request.approve()


async def on_startup() -> None:
    await Tortoise.init(
        db_url=config.DB_URL.get_secret_value(),
        modules={"models": ["db.models.user"]},
    )
    await Tortoise.generate_schemas()

async def on_shutdown() -> None:
    await Tortoise.close_connections()

async def main():

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())