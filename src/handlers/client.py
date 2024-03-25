from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import ChatJoinRequest
from loguru import logger

from config_reader import config, google_sheet
from utils.func import send_message, req_user
from db.models import User


router = Router()


@router.chat_join_request(F.chat.id == int(config.CHANNEL_ID.get_secret_value()))
async def chat_join_handler(request: ChatJoinRequest):
    try:
        await request.approve()
    except:
        logger.warning("Chat join request failed")
    await req_user(request)


@router.message(F.text == "req")
async def req_handler(message: Message):
    await req_user(message)


@router.message(F.text == "q")
async def req_handler(message: Message):
    print(message.from_user.id)


@router.message()
async def message_handler(message: Message):
    user = await User.get_or_none(user_id=message.from_user.id)
    if user is not None:
        chat_id = user.chat_id
        if user.topic_id is not None:
            await send_message(message, chat_id, user.topic_id)
        else:
            name = f"{message.from_user.full_name} #{message.from_user.id}"
            topic = await message.bot.create_forum_topic(chat_id, name=name)
            topic_id = topic.message_thread_id
            google_sheet.update_fm(message.from_user.id)
            await send_message(message, chat_id, topic_id)
            await user.update_from_dict({"topic_id": topic_id, "state": 5})
            await user.save()
    else:
        print("Not user")
