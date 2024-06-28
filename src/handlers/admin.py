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
menu_main = ["First Message", "Push Message", "Push time", "Push Message2", "Push time2", "Push Message3", "Push time3"]

@router.message(StateFilter("*"), F.text == "Back")
async def admin_back_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Menu:",
        reply_markup=get_keyboard(menu_main),
    )


@router.message(AdminFilter(), F.text == "Push time")
async def push_time_handler(message: Message):
    await message.answer(
        f"Push time: {config.time_to_push} minutes",
        reply_markup=get_keyboard(["Set push time", "Back"], 1),
    )


@router.message(AdminFilter(), F.text == "Push time2")
async def push_time_handler2(message: Message):
    await message.answer(
        f"Push time: {config.time_to_push2} minutes",
        reply_markup=get_keyboard(["Set push time2", "Back"], 1),
    )


@router.message(AdminFilter(), F.text == "Push time3")
async def push_time_handler3(message: Message):
    await message.answer(
        f"Push time: {config.time_to_push3} minutes",
        reply_markup=get_keyboard(["Set push time3", "Back"], 1),
    )

@router.message(AdminFilter(), F.text == "Set push time")
async def add_time_handler(message: Message, state: FSMContext):
    await state.set_state(AddChat.add_chat)
    await state.set_data({"push_time":1})
    await message.answer(
        "Type minutes:", reply_markup=get_keyboard(["Back"])
    )


@router.message(AdminFilter(), F.text == "Set push time2")
async def add_time_handler2(message: Message, state: FSMContext):
    await state.set_state(AddChat.add_chat)
    await state.set_data({"push_time":2})
    await message.answer(
        "Type minutes:", reply_markup=get_keyboard(["Back"])
    )


@router.message(AdminFilter(), F.text == "Set push time3")
async def add_time_handler3(message: Message, state: FSMContext):
    await state.set_state(AddChat.add_chat)
    await state.set_data({"push_time":3})
    await message.answer(
        "Type minutes:", reply_markup=get_keyboard(["Back"])
    )


@router.message(AdminFilter(), AddChat.add_chat)
async def finish_time_chat(message: Message, state: FSMContext):
    try:
        time = int(message.text)
        data = await state.get_data()
        push_time = data["push_time"]
        if push_time == 1:
            config.time_to_push = time
        elif push_time == 2:
            config.time_to_push2 = time
        elif push_time == 3:
            config.time_to_push3 = time
        await state.clear()
        await message.answer(
            "time successfully added",
            reply_markup=get_keyboard(menu_main),
        )
    except:
        await message.answer(
            "Invalid time format", reply_markup=get_keyboard(["Back"])
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
@router.message(AdminFilter(), F.text == "Push Message2")
async def push_message_handler2(message: Message):
    if config.push_message2 == None:
        await message.answer(
            "Push message is not set",
            reply_markup=get_keyboard(["Set Push Message2", "Back"], 1),
        )
    else:
        await send_message(
            config.push_message2,
            message.chat.id,
            reply_markup=get_keyboard(
                ["View Push Message2", "Set Push Message2", "Back"], 1
            ),
        )
@router.message(AdminFilter(), F.text == "Push Message3")
async def push_message_handler3(message: Message):
    if config.push_message3 == None:
        await message.answer(
            "Push message is not set",
            reply_markup=get_keyboard(["Set Push Message3", "Back"], 1),
        )
    else:
        await send_message(
            config.push_message3,
            message.chat.id,
            reply_markup=get_keyboard(
                ["View Push Message3", "Set Push Message3", "Back"], 1
            ),
        )


@router.message(AdminFilter(), F.text == "Set First Message")
async def set_first_message_handler(message: Message, state: FSMContext):
    await state.set_state(FirstMessage.first)
    await message.answer("Send first message", reply_markup=get_keyboard(["Back"], 1))


@router.message(AdminFilter(), FirstMessage.first)
async def set_first_message_handler2(message: Message, state: FSMContext):
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
    await state.set_data({"push_message":1})
    await message.answer("Send push message", reply_markup=get_keyboard(["Back"], 1))


@router.message(AdminFilter(), F.text == "Set Push Message2")
async def set_push_message_handler(message: Message, state: FSMContext):
    await state.set_state(PushMessage.push)
    await state.set_data({"push_message":2})
    await message.answer("Send push message", reply_markup=get_keyboard(["Back"], 1))


@router.message(AdminFilter(), F.text == "Set Push Message3")
async def set_push_message_handler(message: Message, state: FSMContext):
    await state.set_state(PushMessage.push)
    await state.set_data({"push_message":3})
    await message.answer("Send push message", reply_markup=get_keyboard(["Back"], 1))


@router.message(AdminFilter(), PushMessage.push)
async def set_push_message_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    push_message = data["push_message"]
    await state.clear()
    if push_message == 1:
        config.push_message = message
        await message.answer(
        "Done",
        reply_markup=get_keyboard(["View Push Message", "Set Push Message", "Back"], 1),
    )
    elif push_message == 2:
        config.push_message2 = message
        await message.answer(
        "Done",
        reply_markup=get_keyboard(["View Push Message2", "Set Push Message2", "Back"], 1),
    )
    elif push_message == 3:
        config.push_message3 = message
        await message.answer(
        "Done",
        reply_markup=get_keyboard(["View Push Message3", "Set Push Message3", "Back"], 1),
    )
        

    
    


@router.message(AdminFilter(), F.text == "View Push Message")
async def view_push_message_handler(message: Message):
    await send_message(
        config.push_message,
        message.chat.id,
        reply_markup=get_keyboard(["View Push Message", "Set Push Message", "Back"], 1),
    )


@router.message(AdminFilter(), F.text == "View Push Message2")
async def view_push_message_handler(message: Message):
    await send_message(
        config.push_message2,
        message.chat.id,
        reply_markup=get_keyboard(["View Push Message2", "Set Push Message2", "Back"], 1),
    )


@router.message(AdminFilter(), F.text == "View Push Message3")
async def view_push_message_handler(message: Message):
    await send_message(
        config.push_message3,
        message.chat.id,
        reply_markup=get_keyboard(["View Push Message3", "Set Push Message3", "Back"], 1),
    )


@router.message(AdminFilter())
async def admin_handler(message: Message):
    await message.answer(
        "Menu:",
        reply_markup=get_keyboard(menu_main),
    )
