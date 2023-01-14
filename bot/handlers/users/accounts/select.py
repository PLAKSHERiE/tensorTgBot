from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter

from keyboards.inline.accounts.menu import cb_account_settings, make_account_markup, PROPERTY_VIEW_ACCOUNT
from loader import dp
from utils.db_api.schemas.account_function import AccountFunction
from utils.misc.account import get_text_account


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                           cb_account_settings.filter(property=PROPERTY_VIEW_ACCOUNT, value='select'),
                           )
async def cq_account_view(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    account_id = int(callback_data.get('id'))
    account = await AccountFunction().get_account_by_id(account_id)
    text = get_text_account(account)
    markup = await make_account_markup(account)
    await call.message.edit_text('\n'.join(text), reply_markup=markup)
