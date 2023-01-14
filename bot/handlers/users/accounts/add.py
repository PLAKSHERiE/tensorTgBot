import logging

import emoji
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import ChatTypeFilter

from keyboards.default.cancel import make_cancel
from keyboards.default.main_menu import user_menu
from keyboards.inline.accounts.data_display import make_data_display_markup, cb_account_data_display, \
    cb_account_data_display_complete, DATA_DISPLAY
from keyboards.inline.accounts.menu import cb_accounts_settings, PROPERTY_ADD_ACCOUNT
from keyboards.inline.accounts.period import make_period_update_markup, cb_account_period_update
from loader import dp
from services.tensor.api import TensorAPI
from states.account import AccountAdd, AccountCheck
from utils.misc.account import get_text_account_data_display
from utils.db_api.schemas.account_function import AccountFunction
from utils.set_bot_commands import COMMANDS


TITLES = [
    '<b>1. Напишите логин:</b>',
    '<b>2. Напишите пароль:</b>',
    '<b>3. Выберите период обновления запросов к API:</b>',
    '<b>4. Выберите какие данные выводить:</b>',
]


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                    text=f'{emoji.emojize(":cross_mark:")} Отмена',
                    state=AccountAdd)
@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                    text=COMMANDS,
                    state=AccountAdd)
async def account_add_cancel(message: types.Message, state: FSMContext):
    """
    Отмена добавления аккаунта
    """
    await state.finish()
    await message.answer(f'{emoji.emojize(":cross_mark:")} Отмена добавления аккаунта', reply_markup=user_menu)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                           cb_accounts_settings.filter(property=PROPERTY_ADD_ACCOUNT, value='select'),
                           )
async def cq_account_add(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Нажатие на Добавить аккаунт
    """
    await call.answer()
    await state.finish()
    await AccountAdd.LOGIN.set()
    await call.message.edit_text('Добавление аккаунта, данные нужны для доступа к API')
    await call.message.answer(TITLES[0], reply_markup=make_cancel())


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                    state=AccountAdd.LOGIN)
async def cq_account_add_login(message: types.Message, state: FSMContext):
    """
    Прием логина
    """
    login = message.text.strip()
    check = await AccountFunction().check_account_exist(message.from_user.id, login)
    if check:
        await state.finish()
        return await message.answer(f'Вы уже добавили этот аккаунт', reply_markup=user_menu)
    await state.update_data(login=login)
    await message.answer(TITLES[1])
    await AccountAdd.PASSWORD.set()


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                    state=AccountAdd.PASSWORD)
async def cq_account_add_password(message: types.Message, state: FSMContext):
    """
    Прием пароля
    """
    password = message.text.strip()
    await state.update_data(password=password)
    markup = await make_period_update_markup()
    await message.answer(TITLES[2], reply_markup=markup)
    await AccountAdd.PERIOD_UPDATE.set()


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                           cb_account_period_update.filter(),
                           state=AccountAdd.PERIOD_UPDATE
                           )
async def cq_account_add_period_update(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Выбор периода обновления API
    """
    await call.answer()
    period = int(callback_data.get('period'))
    data_display = [0, 1, 2]
    await state.update_data(period_update=period)
    await state.update_data(data_display=data_display)
    markup = await make_data_display_markup(data_display, next_button='Продолжить')
    await call.message.edit_text("\n".join(get_text_account_data_display(TITLES[3])), reply_markup=markup)
    await AccountAdd.DATA_DISPLAY.set()


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                           cb_account_data_display.filter(),
                           state=AccountAdd.DATA_DISPLAY
                           )
async def cq_account_add_data_display(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Выбор отображаемых данных
    """
    await call.answer()
    state_data = await state.get_data()
    data_index = int(callback_data.get('data_index'))
    new_data_display = state_data['data_display']
    if data_index not in new_data_display:
        new_data_display.append(data_index)
    else:
        new_data_display.remove(data_index)
    await state.update_data(data_display=new_data_display)
    markup = await make_data_display_markup(new_data_display, next_button='Продолжить')
    await call.message.edit_text("\n".join(get_text_account_data_display(TITLES[3])), reply_markup=markup)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                           cb_account_data_display_complete.filter(value='true'),
                           state=AccountAdd.DATA_DISPLAY
                           )
async def cq_account_add_data_display_complete(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Конечное создание аккаунта
    """
    await call.answer()
    state_data = await state.get_data()
    state_data['data_display'] = [DATA_DISPLAY[i] for i in state_data['data_display']]

    await call.message.edit_text('Проверка валидности данных...')
    await AccountCheck.CHECK_ACCOUNT.set()
    api = TensorAPI(state_data['login'], state_data['password'])

    try:
        result = await api.auth()
        # print(result)
        if api.ERROR_AUTH:
            await call.message.delete()
            return await call.message.answer(api.ERROR_AUTH, reply_markup=user_menu)

        await AccountFunction().create_account(call, state_data, api.TOKEN)
        await call.message.answer(f'{emoji.emojize(":check_mark_button:")} Аккаунт успешно добавлен',
                                  reply_markup=user_menu)
    except Exception as e:
        error = 'Ошибка в добавлении аккаунта'
        logging.error(e)
        await call.message.delete()
        await call.message.answer(error, reply_markup=user_menu)
