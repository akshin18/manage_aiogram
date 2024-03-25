from aiogram import Router, F
from aiogram.types import Message, ContentType
from loguru import logger

from config_reader import config, google_sheet
from db.models import User
from utils.func import send_message


router = Router()


@router.message(F.chat.id.in_(config.CHAT_IDS), F.text == "finish#")
async def finish_handler(message: Message):
    topic_name = message.reply_to_message.forum_topic_created.name
    old_topic_id = message.reply_to_message.message_thread_id
    topic = await message.bot.create_forum_topic(config.LAST_CHAT_ID, name=topic_name)
    topic_id = topic.message_thread_id
    user = await User.get(topic_id=old_topic_id, chat_id=message.chat.id)
    google_sheet.update_finish(user.user_id)
    await user.update_from_dict({"topic_id": topic_id, "chat_id": config.LAST_CHAT_ID, "state": 6})
    await user.save()


@router.message(F.chat.id.in_([*config.CHAT_IDS, config.LAST_CHAT_ID]))
async def message_handler(message: Message):
    logger.info("Message from manager")
    if message.text == None and message.content_type == ContentType.TEXT:
        return
    else:
        logger.info("Message manager pass")
        chat_id = message.chat.id
        try:
            topic_id = message.reply_to_message.message_thread_id
        except:
            logger.warning("Message from manager without reply")
            return
        user = await User.get_or_none(chat_id=chat_id, topic_id=topic_id)
        if user is not None:
            try:
                await send_message(message, user.user_id)
            except:
                google_sheet.update_active(user.user_id)
                await message.answer("Юзер заблокировал бота")
