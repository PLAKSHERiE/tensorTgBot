import emoji
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter

from keyboards.default.cancel import make_cancel
from keyboards.default.main_menu import user_menu
from keyboards.inline.accounts.menu import cb_account_settings, PROPERTY_DELETE_ACCOUNT, \
    make_account_delete_confirmation_markup, make_accounts_markup, make_account_markup
from loader import dp
from states.account import AccountDelete
from utils.db_api.schemas.account_function import AccountFunction
from utils.misc.account import get_text_account


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                    text=f'{emoji.emojize(":cross_mark:")} Отмена',
                    state=AccountDelete)
async def account_delete_cancel(message: types.Message, state: FSMContext):
    """
    Отмена удаления аккаунта
    """
    await message.answer(f'{emoji.emojize(":cross_mark:")} Отмена удаления аккаунта', reply_markup=user_menu)
    data = await state.get_data()
    account_id = int(data['id'])
    account = await AccountFunction().get_account_by_id(account_id)
    text = get_text_account(account)
    markup = await make_account_markup(account)
    await message.answer('\n'.join(text), reply_markup=markup)
    await state.finish()


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                           cb_account_settings.filter(property=PROPERTY_DELETE_ACCOUNT, value='select'),
                           )
async def cq_account_delete(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Удаление аккаунта
    """
    account_id = int(callback_data.get('id'))
    await call.answer()
    await AccountDelete.CONFIRM.set()
    current_state = Dispatcher.get_current().current_state()
    await current_state.update_data(id=account_id)
    account = await AccountFunction().get_account_by_id(account_id)
    await call.message.answer('Удаление аккаунта', reply_markup=make_cancel())
    markup = await make_account_delete_confirmation_markup(account)
    await call.message.answer('<b>Вы точно уверены, что хотите удалить аккаунт?</b>', reply_markup=markup)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                           cb_account_settings.filter(property=PROPERTY_DELETE_ACCOUNT, value='confirm'),
                           state=AccountDelete.CONFIRM
                           )
async def cq_account_delete_confirm(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Подтверждение удаления аккаунта
    """
    account_id = int(callback_data.get('id'))
    await AccountFunction().delete_account(account_id)
    await call.message.answer(f'{emoji.emojize(":check_mark_button:")} Аккаунт удален', reply_markup=user_menu)
    await state.finish()
    await call.answer()
    title, markup = await make_accounts_markup(int(call.from_user.id))
    await call.message.answer(title, reply_markup=markup)
