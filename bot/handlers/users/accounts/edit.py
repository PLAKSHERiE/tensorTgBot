import emoji
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter

from keyboards.default.cancel import make_cancel
from keyboards.default.main_menu import user_menu
from keyboards.inline.accounts.data_display import make_data_display_markup, DATA_DISPLAY, cb_account_data_display, \
    cb_account_data_display_complete
from keyboards.inline.accounts.menu import cb_account_settings, PROPERTY_EDIT_ACCOUNT
from keyboards.inline.accounts.period import make_period_update_markup, cb_account_period_update
from loader import dp
from states.account import AccountEdit
from utils.db_api.schemas.account_function import AccountFunction
from utils.misc.account import get_text_account_data_display, get_account_edit_data

UPDATE_SUCCESSFUL = f'{emoji.emojize(":check_mark_button:")} Изменено'
ACCOUNT_NOT_VALID = f'{emoji.emojize(":red_exclamation_mark:")} <b>Невалидные данные от аккаунта</b>, ответ от сервера:'


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                    text=f'{emoji.emojize(":cross_mark:")} Отмена',
                    state=AccountEdit)
async def account_edit_cancel(message: types.Message, state: FSMContext):
    """
    Отмена редактирования аккаунта
    """
    await message.answer(f'{emoji.emojize(":cross_mark:")} Отмена редактирования аккаунта', reply_markup=user_menu)
    data = await state.get_data()
    account_id = int(data['id'])
    account = await AccountFunction().get_account_by_id(account_id)
    text, markup = await get_account_edit_data(account)
    await message.answer('\n'.join(text), reply_markup=markup)
    await state.finish()


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                           cb_account_settings.filter(property=PROPERTY_EDIT_ACCOUNT, value='select'),
                           )
async def cq_account_edit(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Сообщение с редактированием аккаунта
    """
    await call.answer()
    account_id = int(callback_data.get('id'))
    account = await AccountFunction().get_account_by_id(account_id)
    text, markup = await get_account_edit_data(account)
    await call.message.edit_text('\n'.join(text), reply_markup=markup)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                           cb_account_settings.filter(property='login', value='edit'),
                           )
async def cq_account_edit_login(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Редактирование логина
    """
    account_id = int(callback_data.get('id'))
    await call.answer()
    await AccountEdit.LOGIN.set()
    current_state = Dispatcher.get_current().current_state()
    await current_state.update_data(id=account_id)
    await call.message.answer('Введите новый логин', reply_markup=make_cancel())


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                    state=AccountEdit.LOGIN,
                    )
async def account_edit_login(message: types.Message, state: FSMContext):
    """
    Завершение редактирование логина
    """
    data = await state.get_data()
    account_id = int(data['id'])

    await AccountFunction().edit_account_field(account_id, 'login', message.text)
    valid, error = await AccountFunction().check_valid_account(account_id)
    account = await AccountFunction().get_account_by_id(account_id)
    text, markup = await get_account_edit_data(account)
    await message.answer(UPDATE_SUCCESSFUL, reply_markup=user_menu)
    if not valid:
        await message.answer(f'{ACCOUNT_NOT_VALID} <code>{error}</code>')
    else:
        await AccountFunction().edit_account_field(account_id, 'correct', True)
    await message.answer('\n'.join(text), reply_markup=markup)
    await state.finish()


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                           cb_account_settings.filter(property='password', value='edit'),
                           )
async def cq_account_edit_password(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Редактирование пароля
    """
    account_id = int(callback_data.get('id'))
    await call.answer()
    await AccountEdit.PASSWORD.set()
    current_state = Dispatcher.get_current().current_state()
    await current_state.update_data(id=account_id)
    await call.message.answer('Введите новый пароль', reply_markup=make_cancel())


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                    state=AccountEdit.PASSWORD,
                    )
async def account_edit_password(message: types.Message, state: FSMContext):
    """
    Завершение редактирование пароля
    """
    data = await state.get_data()
    account_id = int(data['id'])

    await AccountFunction().edit_account_field(account_id, 'password', message.text)
    valid, error = await AccountFunction().check_valid_account(account_id)
    account = await AccountFunction().get_account_by_id(account_id)
    text, markup = await get_account_edit_data(account)
    await message.answer(UPDATE_SUCCESSFUL, reply_markup=user_menu)
    if not valid:
        await message.answer(f'{ACCOUNT_NOT_VALID} <code>{error}</code>')
    else:
        await AccountFunction().edit_account_field(account_id, 'correct', True)
    await message.answer('\n'.join(text), reply_markup=markup)
    await state.finish()


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                           cb_account_settings.filter(property='period_update', value='edit'),
                           )
async def cq_account_edit_period_update(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Редактирование периода обновлений
    """
    account_id = int(callback_data.get('id'))
    await call.answer()
    await AccountEdit.PERIOD_UPDATE.set()
    current_state = Dispatcher.get_current().current_state()
    await current_state.update_data(id=account_id)
    await call.message.answer('Выберите другой период обновлений', reply_markup=make_cancel())
    markup = await make_period_update_markup()
    await call.message.answer('Периоды обновления API', reply_markup=markup)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                           cb_account_period_update.filter(),
                           state=AccountEdit.PERIOD_UPDATE,
                           )
async def cq_account_edit_period_update_complete(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Завершение редактирование периода обновлений
    """
    data = await state.get_data()
    account_id = int(data['id'])
    period = int(callback_data.get('period'))
    await call.answer()

    await AccountFunction().edit_account_field(account_id, 'period_update', period)
    account = await AccountFunction().get_account_by_id(account_id)
    text, markup = await get_account_edit_data(account)
    await call.message.answer(UPDATE_SUCCESSFUL, reply_markup=user_menu)
    await call.message.answer('\n'.join(text), reply_markup=markup)
    await state.finish()


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                           cb_account_settings.filter(property='data_display', value='edit'),
                           )
async def cq_account_edit_data_display(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Редактирование отображаемых данных
    """
    account_id = int(callback_data.get('id'))
    await call.answer()
    account = await AccountFunction().get_account_by_id(account_id)
    data_display = []
    for index, data in enumerate(DATA_DISPLAY):
        if data in account.data_display:
            data_display.append(index)

    await AccountEdit.DATA_DISPLAY.set()
    current_state = Dispatcher.get_current().current_state()
    await current_state.update_data(
        id=account_id,
        data_display=data_display
    )
    title = get_text_account_data_display('Отображаемые данные')
    await call.message.answer('Выберите отображаемые данные', reply_markup=make_cancel())
    markup = await make_data_display_markup(data_display, next_button='Сохранить')
    await call.message.answer('\n'.join(title), reply_markup=markup)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                           cb_account_data_display.filter(),
                           state=AccountEdit.DATA_DISPLAY,
                           )
async def cq_account_edit_data_display_select(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Выбор отображаемых данных
    """
    data = await state.get_data()
    data_index = int(callback_data.get('data_index'))
    new_data_display = data['data_display']
    if data_index not in new_data_display:
        new_data_display.append(data_index)
    else:
        new_data_display.remove(data_index)
    await state.update_data(data_display=new_data_display)
    await call.answer()
    title = get_text_account_data_display('Отображаемые данные')
    markup = await make_data_display_markup(new_data_display, next_button='Сохранить')
    await call.message.edit_text('\n'.join(title), reply_markup=markup)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                           cb_account_data_display_complete.filter(value='true'),
                           state=AccountEdit.DATA_DISPLAY
                           )
async def cq_account_edit_data_display_complete(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Завершение редактирования отображаемых данных
    """
    data = await state.get_data()
    account_id = int(data['id'])
    await call.answer()
    data_display = [DATA_DISPLAY[i] for i in data['data_display']]
    await AccountFunction().edit_account_field(account_id, 'data_display', data_display)
    account = await AccountFunction().get_account_by_id(account_id)
    text, markup = await get_account_edit_data(account)
    await call.message.answer(UPDATE_SUCCESSFUL, reply_markup=user_menu)
    await call.message.answer('\n'.join(text), reply_markup=markup)
    await state.finish()
