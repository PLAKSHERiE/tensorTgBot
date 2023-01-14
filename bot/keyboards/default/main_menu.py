import emoji
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"{emoji.emojize(':superhero:')} Аккаунты"),
        ]
    ],
    resize_keyboard=True
)
