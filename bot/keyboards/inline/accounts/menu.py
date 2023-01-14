from typing import Tuple

import emoji
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api.schemas.account import Account
from utils.db_api.schemas.account_function import AccountFunction

cb_account_settings = CallbackData("account", "id", "property", "value")
cb_accounts_settings = CallbackData("accounts", "property", "value")

PROPERTY_ALL_ACCOUNTS = 'all'
PROPERTY_VIEW_ACCOUNT = 'view'
PROPERTY_ADD_ACCOUNT = 'add'
PROPERTY_EDIT_ACCOUNT = 'edit'
PROPERTY_DELETE_ACCOUNT = 'delete'


async def make_accounts_markup(user_id: int) -> Tuple[str, InlineKeyboardMarkup]:
    title = f"{emoji.emojize(':superhero:')} Аккаунты"
    markup = InlineKeyboardMarkup(row_width=1)
    accounts = await AccountFunction().get_all_accounts_by_user_id(user_id)
    for account in accounts:
        markup.insert(
            InlineKeyboardButton(
                text=account.login,
                callback_data=cb_account_settings.new(
                    id=account.id, property=PROPERTY_VIEW_ACCOUNT, value='select'
                )
            )
        )
    markup.insert(
        InlineKeyboardButton(
            text=f"{emoji.emojize(':plus:')} Добавить аккаунт",
            callback_data=cb_accounts_settings.new(
                property=PROPERTY_ADD_ACCOUNT, value='select'
            )
        )
    )
    # print(accounts)
    return title, markup


async def make_account_markup(account: Account) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(
        InlineKeyboardButton(
            text=f"{emoji.emojize(':pencil:')} Редактировать",
            callback_data=cb_account_settings.new(
                id=account.id, property=PROPERTY_EDIT_ACCOUNT, value='select'
            )
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text=f"{emoji.emojize(':cross_mark:')} Удалить",
            callback_data=cb_account_settings.new(
                id=account.id, property=PROPERTY_DELETE_ACCOUNT, value='select'
            )
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=f"{emoji.emojize(':reverse_button:')} Назад",
            callback_data=cb_accounts_settings.new(
                property=PROPERTY_ALL_ACCOUNTS, value='select'
            )
        )
    )
    return markup


async def make_account_edit_markup(account: Account) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(
        InlineKeyboardButton(
            text=f"Логин",
            callback_data=cb_account_settings.new(
                id=account.id, property='login', value='edit'
            )
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text=f"Пароль",
            callback_data=cb_account_settings.new(
                id=account.id, property='password', value='edit'
            )
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text=f"Период обновлений",
            callback_data=cb_account_settings.new(
                id=account.id, property='period_update', value='edit'
            )
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text=f"Отображаемые данные",
            callback_data=cb_account_settings.new(
                id=account.id, property='data_display', value='edit'
            )
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=f"{emoji.emojize(':reverse_button:')} Назад",
            callback_data=cb_account_settings.new(
                id=account.id, property=PROPERTY_VIEW_ACCOUNT, value='select'
            )
        )
    )
    return markup


async def make_account_delete_confirmation_markup(account: Account) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(
        InlineKeyboardButton(
            text=f"{emoji.emojize(':cross_mark:')} Удалить",
            callback_data=cb_account_settings.new(
                id=account.id, property=PROPERTY_DELETE_ACCOUNT, value='confirm'
            )
        )
    )
    return markup
