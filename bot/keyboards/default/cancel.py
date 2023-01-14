import emoji
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_cancel():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f'{emoji.emojize(":cross_mark:")} Отмена'),
            ],

        ],
        resize_keyboard=True
    )
    return markup
