import emoji
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import ChatTypeFilter

from keyboards.inline.accounts.menu import make_accounts_markup, cb_accounts_settings, PROPERTY_ALL_ACCOUNTS
from loader import dp
from utils.misc import rate_limit


@rate_limit(3)
@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                    text=f"{emoji.emojize(':superhero:')} Аккаунты",
                    state="*",
                    )
async def accounts(message: types.Message, state: FSMContext):
    await state.finish()
    title, markup = await make_accounts_markup(int(message.from_user.id))
    await message.answer(title, reply_markup=markup)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                           cb_accounts_settings.filter(property=PROPERTY_ALL_ACCOUNTS, value='select'),
                           )
async def cq_accounts(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    title, markup = await make_accounts_markup(int(call.from_user.id))
    await call.message.edit_text(title, reply_markup=markup)
