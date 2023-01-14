from aiogram.dispatcher.filters.state import StatesGroup, State


class AccountAdd(StatesGroup):
    LOGIN = State()
    PASSWORD = State()
    PERIOD_UPDATE = State()
    DATA_DISPLAY = State()


class AccountCheck(StatesGroup):
    CHECK_ACCOUNT = State()


class AccountEdit(StatesGroup):
    LOGIN = State()
    PASSWORD = State()
    PERIOD_UPDATE = State()
    DATA_DISPLAY = State()


class AccountDelete(StatesGroup):
    CONFIRM = State()
