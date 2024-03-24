from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from config_reader import config
from utils.func import send_message
from keyboards.common import get_keyboard
from filters.filter import AdminFilter
from utils.states import FirstMessage, PushMessage, AddChat

router = Router()

# @router.message(AdminFilter())
# async def admin_handler(message: Message):
#     q = await message.bot.get_chat(config.CHAT_IDS[0])
#     print(q)


@router.message(StateFilter("*"), F.text == "Back")
async def admin_back_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Menu:",
        reply_markup=get_keyboard(["First Message", "Push Message", "Add chat"]),
    )


@router.message(AdminFilter(), F.text == "Add chat")
async def add_chat_handler(message: Message, state: FSMContext):
    await state.set_state(AddChat.add_chat)
    await message.answer(
        "Type chat id example: -102100002", reply_markup=get_keyboard(["Back"])
    )


@router.message(AdminFilter(), AddChat.add_chat)
async def finish_add_chat(message: Message, state: FSMContext):
    try:
        chat_id = int(message.text)
        config.CHAT_IDS.append(chat_id)
        await state.clear()
        await message.answer(
            "Chat successfully added",
            reply_markup=get_keyboard(["First Message", "Push Message", "Add chat"]),
        )
    except:
        await message.answer(
            "Invalid chat id format", reply_markup=get_keyboard(["Back"])
        )


@router.message(AdminFilter(), F.text == "First Message")
async def first_message_handler(message: Message):
    if config.first_message == None:
        await message.answer(
            "First message is not set",
            reply_markup=get_keyboard(["Set First Message", "Back"], 1),
        )
    else:
        await send_message(
            config.first_message,
            message.chat.id,
            reply_markup=get_keyboard(
                ["View First Message", "Set First Message", "Back"], 1
            ),
        )


@router.message(AdminFilter(), F.text == "Push Message")
async def push_message_handler(message: Message):
    if config.push_message == None:
        await message.answer(
            "Push message is not set",
            reply_markup=get_keyboard(["Set Push Message", "Back"], 1),
        )
    else:
        await send_message(
            config.push_message,
            message.chat.id,
            reply_markup=get_keyboard(
                ["View Push Message", "Set Push Message", "Back"], 1
            ),
        )


@router.message(AdminFilter(), F.text == "Set First Message")
async def set_first_message_handler(message: Message, state: FSMContext):
    await state.set_state(FirstMessage.first)
    await message.answer("Send first message", reply_markup=get_keyboard(["Back"], 1))


@router.message(AdminFilter(), FirstMessage.first)
async def set_first_message_handler(message: Message, state: FSMContext):
    config.first_message = message
    await state.clear()
    await message.answer(
        "Done",
        reply_markup=get_keyboard(
            ["View First Message", "Set First Message", "Back"], 1
        ),
    )


@router.message(AdminFilter(), F.text == "View First Message")
async def view_first_message_handler(message: Message):
    await send_message(
        config.first_message,
        message.chat.id,
        reply_markup=get_keyboard(
            ["View First Message", "Set First Message", "Back"], 1
        ),
    )


@router.message(AdminFilter(), F.text == "Set Push Message")
async def set_push_message_handler(message: Message, state: FSMContext):
    await state.set_state(PushMessage.push)
    await message.answer("Send push message", reply_markup=get_keyboard(["Back"], 1))


@router.message(AdminFilter(), PushMessage.push)
async def set_push_message_handler(message: Message, state: FSMContext):
    config.push_message = message
    await state.clear()
    await message.answer(
        "Done",
        reply_markup=get_keyboard(["View Push Message", "Set Push Message", "Back"], 1),
    )


@router.message(AdminFilter(), F.text == "View Push Message")
async def view_push_message_handler(message: Message):
    await send_message(
        config.push_message,
        message.chat.id,
        reply_markup=get_keyboard(["View Push Message", "Set Push Message", "Back"], 1),
    )


@router.message(AdminFilter())
async def admin_handler(message: Message):
    await message.answer(
        "Menu:",
        reply_markup=get_keyboard(["First Message", "Push Message", "Add chat"]),
    )