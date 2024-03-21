from typing import Union

from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_keyboard(names: Union[str, list], adjust:int = 2):
    if type(names) == str:
        names = [names]
    builder = ReplyKeyboardBuilder()
    for name in names:
        builder.button(text=name)
    builder.adjust(adjust)
    return builder.as_markup()
    
