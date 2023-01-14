import emoji
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

cb_account_data_display = CallbackData('account_data_display', 'data_index')
cb_account_data_display_complete = CallbackData('account_data_display_complete', 'value')

# Галка, крест
FLAG_STATUS = [f'{emoji.emojize(":cross_mark:")}', f'{emoji.emojize(":check_mark_button:")}']

DATA_DISPLAY = [
    'Изменение лицензии',
    'Привязка тарифа',
    'Отгрузка лицензии',
    'Заявка на подключение',
    'Реквизиты и контакты',
    'Добавление контрагента',
    'Удаление контрагента',
    'Подключение ЭДО',
    'Отключение ЭДО',
    'Подключение ЭО',
    'Отключение ЭО',
    'Подключение Роуминга',
    'Получение закрепления',
    'Потеря закрепления',
    'Выставлен счет',
    'Подключение акции',
    'Блокирование лицензии',
]


async def make_data_display_markup(active: list, next_button: str = None) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=4)
    for index, data in enumerate(DATA_DISPLAY):
        icon = FLAG_STATUS[0]
        if index in active:
            icon = FLAG_STATUS[1]
        markup.insert(
            InlineKeyboardButton(
                text=f'{icon} {index + 1}',
                callback_data=cb_account_data_display.new(
                    data_index=index
                )
            )
        )
    if next_button:
        markup.row(
            InlineKeyboardButton(
                text=f'{next_button}',
                callback_data=cb_account_data_display_complete.new(
                    value='true'
                )
            )
        )

    return markup
