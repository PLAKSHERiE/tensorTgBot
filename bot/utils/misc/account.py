from typing import Tuple

import emoji
from aiogram.types import InlineKeyboardMarkup

from keyboards.inline.accounts.data_display import DATA_DISPLAY
from keyboards.inline.accounts.menu import make_account_edit_markup
from utils.db_api.schemas.account import Account


def get_text_account_data_display(title: str = '') -> list:
    """
    Текст отображаемых данных из API
    """
    text = [
        title,
        '',
    ]
    [text.append(f'{index + 1}. {data}') for index, data in enumerate(DATA_DISPLAY)]
    return text


def get_text_account(account: Account,
                     title: str = f'{emoji.emojize(":diamond_with_a_dot:")} <b>Информация об аккаунте</b>') -> list:
    """
    Текст с подробностями аккаунта
    """
    text = [
        title,
        '',
        f'<b>Логин:</b> <code>{account.login}</code>',
        f'<b>Пароль:</b> <code>{account.password}</code>',
        f'<b>Период обновлений API:</b> {account.period_update} мин.',
    ]
    data_display = 'Нет'
    if account.data_display:
        data_display = ', '.join(account.data_display)
    text.append(f'<b>Отображаемые данные:</b> {data_display}')
    if not account.correct:
        text.extend([
            '',
            f'{emoji.emojize(":red_exclamation_mark:")} <b>Логин или пароль стали некорректны</b>'
        ])

    return text


async def get_account_edit_data(account: Account) -> Tuple[list, InlineKeyboardMarkup]:
    """
    Текст и меню редактирования аккаунта
    """
    text = get_text_account(account, title=f'{emoji.emojize(":pencil:")} <b>Редактирование аккаунт</b>')
    markup = await make_account_edit_markup(account)
    return text, markup
