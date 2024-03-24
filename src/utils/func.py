import datetime
import asyncio
import logging
from typing import Union

from aiogram.types import Message, ChatJoinRequest, ContentType

from config_reader import config, google_sheet
from db.models import User
from app import bot


async def send_message(
    message: Message, chat_id: int, topic_id: Union[int, None] = None, reply_markup=None
):
    try:
        if message.content_type == ContentType.TEXT:
            await message.bot.send_message(
                chat_id,
                text=message.text,
                message_thread_id=topic_id,
                reply_markup=reply_markup,
            )
        elif message.content_type == ContentType.PHOTO:
            await message.bot.send_photo(
                chat_id,
                photo=message.photo[0].file_id,
                message_thread_id=topic_id,
                caption=message.caption,
                reply_markup=reply_markup,
            )
        elif message.content_type == ContentType.VIDEO:
            await message.bot.send_video(
                chat_id,
                video=message.video.file_id,
                message_thread_id=topic_id,
                caption=message.caption,
                reply_markup=reply_markup,
            )
        elif message.content_type == ContentType.DOCUMENT:
            await message.bot.send_document(
                chat_id,
                document=message.document.file_id,
                message_thread_id=topic_id,
                caption=message.caption,
                reply_markup=reply_markup,
            )
        elif message.content_type == ContentType.STICKER:
            await message.bot.send_sticker(
                chat_id,
                sticker=message.sticker.file_id,
                message_thread_id=topic_id,
                reply_markup=reply_markup,
            )
        elif message.content_type == ContentType.AUDIO:
            await message.bot.send_audio(
                chat_id,
                audio=message.audio.file_id,
                message_thread_id=topic_id,
                caption=message.caption,
                reply_markup=reply_markup,
            )
        elif message.content_type == ContentType.VOICE:
            await message.bot.send_voice(
                chat_id,
                voice=message.voice.file_id,
                message_thread_id=topic_id,
                reply_markup=reply_markup,
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
        chat_id=config.CHAT_IDS[config.manager_index],
        invite_link=message.invite_link.invite_link if isinstance(message, ChatJoinRequest) else "None"
    )
    add_user_to_sheet(user)
    if config.first_message != None:
        await send_message(config.first_message, message.from_user.id)
    else:
        if config.ADMINS_ID != []:
            await bot.send_message(config.ADMINS_ID[0],text="Нет Первого сообщения")
            await message.bot.send_message(message.from_user.id, "))")

def add_user_to_sheet(user:User):
    google_sheet.create_user(
        user.created_at.strftime("%d/%m/%Y %H:%M"),
        user.user_id,
        user.chat_id,
        user.invite_link,
        "true",
        username=user.username,
    )

async def check_push() -> None:
    while True:
        now = datetime.datetime.now()
        one_hour_ago = now - datetime.timedelta(hours=1)

        users = await User.filter(state=0, created_at__lt=one_hour_ago)

        for user in users:
            if config.push_message != None:
                await user.update_from_dict({"state": 1})
                await user.save()
                await send_message(config.push_message, user.user_id)
            else:
                if config.ADMINS_ID != []:
                    await bot.send_message(config.ADMINS_ID[0],text="Нет пуша")

        users = await User.filter(state=1, updated_at__lt=one_hour_ago)

        for user in users:
            await user.update_from_dict({"state": 5})
            await user.save()
            chat_id = config.CHAT_IDS[user.manager_index]
            name = f"{user.name} #{user.user_id}"
            topic = await bot.create_forum_topic(chat_id, name=name)
            topic_id = topic.message_thread_id
            await bot.send_message(
                chat_id,
                text="Пользователь не ответил на пуш",
                message_thread_id=topic_id,
            )
        logging.info("Check push done")
        await asyncio.sleep(60 * 10)
