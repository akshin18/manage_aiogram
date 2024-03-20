import asyncio
import logging
from typing import Union

from aiogram.types import Message, ChatJoinRequest, ForumTopicCreated
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ContentType
from aiogram import Bot, Dispatcher, F
from tortoise import Tortoise
from db.models import User

from config_reader import config


bot = Bot(
    config.BOT_TOKEN.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()


@dp.chat_join_request(F.chat.id == int(config.CHANNEL_ID.get_secret_value()))
async def chat_join_handler(request: ChatJoinRequest):
    await request.approve()
    await req_user(request)


@dp.message(F.text == "req")
async def req_handler(message: Message):
    await req_user(message)


@dp.message(F.chat.id.in_(config.CHAT_IDS))
async def message_handler(message: Message):
    if message.text != None:
        chat_id = message.chat.id
        chat_index = config.CHAT_IDS.index(chat_id)
        topic_id = message.reply_to_message.message_thread_id
        user = await User.get_or_none(manager_index=chat_index, topic_id=topic_id)
        if user is not None:
            await send_message(message, user.user_id)


@dp.message()
async def message_handler(message: Message):
    user = await User.get_or_none(user_id=message.from_user.id)
    if user is not None:
        chat_id = config.CHAT_IDS[user.manager_index]
        if user.topic_id is not None:
            await send_message(message, chat_id, user.topic_id)
        else:
            name = f"{message.from_user.full_name} #{message.from_user.id}"
            topic = await message.bot.create_forum_topic(chat_id, name=name)
            topic_id = topic.message_thread_id
            await send_message(message, chat_id, topic_id)
            await user.update_from_dict({"topic_id": topic_id, "state": 5})
            await user.save()
    else:
        print("Not user")


async def send_message(
    message: Message, chat_id: int, topic_id: Union[int, None] = None
):
    try:
        if message.content_type == ContentType.TEXT:
            await message.bot.send_message(
                chat_id, text=message.text, message_thread_id=topic_id
            )
        elif message.content_type == ContentType.PHOTO:
            await message.bot.send_photo(
                chat_id,
                photo=message.photo[0].file_id,
                message_thread_id=topic_id,
                caption=message.caption,
            )
        elif message.content_type == ContentType.VIDEO:
            await message.bot.send_video(
                chat_id,
                video=message.video.file_id,
                message_thread_id=topic_id,
                caption=message.caption,
            )
        elif message.content_type == ContentType.DOCUMENT:
            await message.bot.send_document(
                chat_id,
                document=message.document.file_id,
                message_thread_id=topic_id,
                caption=message.caption,
            )
        elif message.content_type == ContentType.STICKER:
            await message.bot.send_sticker(
                chat_id, sticker=message.sticker.file_id, message_thread_id=topic_id
            )
        elif message.content_type == ContentType.AUDIO:
            await message.bot.send_audio(
                chat_id,
                audio=message.audio.file_id,
                message_thread_id=topic_id,
                caption=message.caption,
            )
        elif message.content_type == ContentType.VOICE:
            await message.bot.send_voice(
                chat_id, voice=message.voice.file_id, message_thread_id=topic_id
            )
        else:
            print("Error")
    except:
        if message.chat.id in config.CHAT_IDS:
            await message.answer("Бот заблокирован!!!!!!")


async def req_user(message: Union[Message, ChatJoinRequest]):
    if config.manager_index + 1 >= len(config.CHAT_IDS):
        config.manager_index = 0
    else:
        config.manager_index += 1
    user, created = await User.get_or_create(
        name=message.from_user.full_name,
        username=message.from_user.username,
        user_id=message.from_user.id,
        manager_index=config.manager_index,
    )
    await message.bot.send_message(message.from_user.id, text="Hello")


async def on_startup() -> None:
    await Tortoise.init(
        db_url=config.DB_URL.get_secret_value(),
        modules={"models": ["db.models"]},
    )
    await Tortoise.generate_schemas()


async def on_shutdown() -> None:
    await Tortoise.close_connections()


async def main():

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
