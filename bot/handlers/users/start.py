from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, ChatTypeFilter

from keyboards.default.main_menu import user_menu
from loader import dp
from utils.misc import rate_limit


@rate_limit(3)
@dp.message_handler(CommandStart(),
                    ChatTypeFilter(chat_type=types.ChatType.PRIVATE)
                    )
async def bot_start(message: types.Message):
    await message.answer(f"Главное меню", reply_markup=user_menu)
