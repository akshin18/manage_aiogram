from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_admin_menu():
    buttons = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="First Message"),
                KeyboardButton(text="Push Message"),  
                KeyboardButton(text="Push Message2"),  
                KeyboardButton(text="Push Message3"),  
            ]
        ],
        resize_keyboard=True
    )
    return buttons