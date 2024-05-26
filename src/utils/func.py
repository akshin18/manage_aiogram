import datetime
import asyncio
import logging
from typing import Union
from traceback import format_exc

from aiogram.types import Message, ChatJoinRequest, ContentType
from loguru import logger
import pytz

from config_reader import config, google_sheet
from db.models import User
from app import bot


async def send_message(
    message: Message, chat_id: int, topic_id: Union[int, None] = None, reply_markup=None
):
    try:
        if isinstance(message, Message):
            if message.content_type == ContentType.TEXT:
                await message.bot.send_message(
                    int(chat_id),
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
            elif message.content_type == ContentType.VIDEO_NOTE:
                await message.bot.send_video_note(
                    chat_id,
                    video_note=message.video_note.file_id,
                    message_thread_id=topic_id,
                    reply_markup=reply_markup,
                )
        elif isinstance(message, str):
            await bot.send_message(
                chat_id,
                text=message,
                message_thread_id=topic_id,
                reply_markup=reply_markup,
            )
        else:
            logger.warning(f"Error, {message.content_type}")
    except Exception as e:
        logger.error("User blocked bot")
        logger.error(str(chat_id))
        logger.error(str(format_exc()))
        if isinstance(message, Message):
            if message.chat.id in [*config.CHAT_IDS, config.LAST_CHAT_ID]:
                google_sheet.update_active(chat_id)
                await message.answer("Бот заблокирован!!!!!!")
        else:
            logger.warning(f"Error in send_message {e}")


async def req_user(message: Union[Message, ChatJoinRequest], req=False):
    if config.manager_index + 1 >= len(config.CHAT_IDS):
        config.manager_index = 0
    else:
        config.manager_index += 1
    user, created = await User.get_or_create(
        name=message.from_user.full_name,
        username=message.from_user.username,
        user_id=message.from_user.id,
        chat_id=config.CHAT_IDS[config.manager_index],
        invite_link=(
            message.invite_link.invite_link
            if isinstance(message, ChatJoinRequest)
            else "None"
        ),
    )
    add_user_to_sheet(user)
    if not created:
        user.update_from_dict({"state": 0})
        await user.save()
    if config.first_message != None:
        await send_message(config.first_message, message.from_user.id)
    else:
        if config.ADMINS_ID != []:
            await bot.send_message(config.ADMINS_ID[0], text="Нет Первого сообщения")
            try:
                await message.bot.send_message(message.from_user.id, "))")
            except:
                google_sheet.update_active(message.from_user.id)

    if req:
        chat_id = user.chat_id
        name = f"{message.from_user.full_name} #{message.from_user.id}"
        topic = await message.bot.create_forum_topic(chat_id, name=name)
        topic_id = topic.message_thread_id
        google_sheet.update_fm(message.from_user.id)
        await send_message(message, chat_id, topic_id)
        await user.update_from_dict({"topic_id": topic_id, "state": 5})
        await user.save()


def add_user_to_sheet(user: User):
    google_sheet.create_user(
        user.created_at.strftime("%d/%m/%Y"),
        user.created_at.strftime("%H:%M"),
        user.user_id,
        user.chat_id,
        user.invite_link,
        "true",
        username=user.username,
    )


async def check_push() -> None:
    moscow_tz = pytz.timezone('Europe/Moscow')
    while True:
        try:
            now = datetime.datetime.now(moscow_tz)
            spec_time = now - datetime.timedelta(minutes=config.time_to_push)
            one_hour_ago = now - datetime.timedelta(minutes=1)
            logger.info(f"Check push at {now}")
            logger.info(f"spec_time {spec_time}")

            users = await User.filter(state=0, created_at__lt=spec_time)
            logger.info(f"Push Users count {len(users)}")
            
            for user in users:
                logger.info(f"send push to {user.name=} {user.user_id=} {user.state=} {user.chat_id=} {user.username=} ")
                if config.push_message != None:
                    try:
                        await send_message(config.push_message, user.user_id)
                        await user.update_from_dict({"state": 1})
                        await user.save()
                        logger.info(f"Push message to {user.user_id}")
                    except:
                        logger.warning(f"Push message to {user.user_id}")
                        google_sheet.update_active(user.user_id)

                else:
                    if config.ADMINS_ID != []:
                        await bot.send_message(config.ADMINS_ID[0], text="Нет пуша")
                    try:
                        await bot.send_message(user.user_id, text="Привет еще раз")
                        await user.update_from_dict({"state": 1})
                        await user.save()
                        logger.success(f"Push message to {user.user_id}")
                    except:
                        logger.warning(f"Push message to {user.user_id}")
                        google_sheet.update_active(user.user_id)

            users = await User.filter(state=1, updated_at__lt=one_hour_ago)
            logger.info(f"Topic Users count {len(users)}")

            for user in users:
                chat_id = user.chat_id
                name = f"{user.name} #{user.user_id}"
                topic = await bot.create_forum_topic(chat_id, name=name)
                topic_id = topic.message_thread_id
                await user.update_from_dict({"state": 5, "topic_id": topic_id})
                await user.save()
                try:
                    await bot.send_message(
                        chat_id,
                        text="Пользователь не ответил на пуш",
                        message_thread_id=topic_id,
                    )
                    google_sheet.auto(user.user_id)
                except:
                    google_sheet.update_active(user.user_id)
            logging.info("Check push done")
            await asyncio.sleep(60)
        except Exception as e:
            logger.error(f"Check push error: {e}")
            await asyncio.sleep(60)