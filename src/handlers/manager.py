from aiogram import Router, F
from aiogram.types import Message, ContentType
from loguru import logger

from config_reader import config, google_sheet
from db.models import User
from utils.func import send_message


router = Router()

@router.message(F.chat.id.in_(config.CHAT_IDS), F.text == "dep#")
async def def_handler(message: Message):
    user = await User.get(chat_id=message.chat.id, topic_id=message.message_thread_id)
    if user != None:
        google_sheet.dep(user.user_id)

@router.message(F.chat.id.in_(config.CHAT_IDS), F.text.startswith("reg#"))
async def reg_handler(message: Message):
    user = await User.get(chat_id=message.chat.id, topic_id=message.message_thread_id)
    if user != None:
        reg_id = message.text.strip().split(" ")[-1]
        user.reg_id = reg_id
        await user.save()
        google_sheet.reg(user.user_id,reg_id)

@router.message(F.chat.id.in_(config.CHAT_IDS),F.text.startswith("geo#"))
async def geo_handler(message: Message):
    geo = message.text.split(" ")[1]
    user = await User.get(chat_id=message.chat.id, topic_id=message.message_thread_id)
    if user != None:
        google_sheet.geo(user.user_id, geo)

@router.message(F.chat.id.in_(config.CHAT_IDS), F.text == "finish#")
async def finish_handler(message: Message):
    topic_name = message.reply_to_message.forum_topic_created.name
    old_topic_id = message.reply_to_message.message_thread_id
    topic = await message.bot.create_forum_topic(config.LAST_CHAT_ID, name=topic_name)
    topic_id = topic.message_thread_id
    user = await User.get_or_none(topic_id=old_topic_id, chat_id=message.chat.id)
    if user != None:
        google_sheet.update_finish(user.user_id)
        await user.update_from_dict({"topic_id": topic_id, "chat_id": config.LAST_CHAT_ID, "state": 6})
        await user.save()
        await message.bot.send_message(
                    user.chat_id,
                    text=f"«ID: {user.reg_id}»",
                    message_thread_id=topic_id
                )
    else:
        await message.answer("Не найден юзер")


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
            user = await User.get_or_none(chat_id=chat_id, topic_id=topic_id)
            if user is not None:
                try:
                    await send_message(message, user.user_id)
                except Exception as e:
                    logger.warning("User blocked bot")
                    logger.warning(str(e))
                    google_sheet.update_active(user.user_id)
                    await message.answer("Юзер заблокировал бота")
        except:
            logger.warning("Message from manager without reply")
            return
        
