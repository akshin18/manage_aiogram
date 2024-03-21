from aiogram import Router, F
from aiogram.types import Message

from config_reader import config
from db.models import User
from utils.func import send_message


router = Router()


@router.message(F.chat.id.in_(config.CHAT_IDS))
async def message_handler(message: Message):
    if message.text != None:
        chat_id = message.chat.id
        chat_index = config.CHAT_IDS.index(chat_id)
        topic_id = message.reply_to_message.message_thread_id
        user = await User.get_or_none(manager_index=chat_index, topic_id=topic_id)
        if user is not None:
            await send_message(message, user.user_id)
