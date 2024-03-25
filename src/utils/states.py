from aiogram.fsm.state import StatesGroup, State


class FirstMessage(StatesGroup):
    first = State()


class PushMessage(StatesGroup):
    push = State()


class AddChat(StatesGroup):
    add_chat = State()
