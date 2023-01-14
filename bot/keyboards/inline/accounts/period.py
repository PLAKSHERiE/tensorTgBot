from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

cb_account_period_update = CallbackData('account_period', 'period')

PERIODS = [
    5,
    15,
    30,
    60,
]


async def make_period_update_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    for period in PERIODS:
        markup.insert(
            InlineKeyboardButton(
                text=f'{period} мин.',
                callback_data=cb_account_period_update.new(
                    period=period
                )
            )
        )

    return markup
