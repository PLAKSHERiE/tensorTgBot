from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from utils.db_api.schemas.user import User, UserFunction


async def check_role(message: Message):
    user_db = await UserFunction().get_user_by_tg_id(message.from_user.id)
    # if not user_db:
    #     await UserFunction().create_user(message)
        # return 1
    # else:
        # await user_db.update_user_info(message)
        # return user_db.role
    return True


class IsUser(BoundFilter):
    async def check(self, message: types.Message):
        return await check_role(message)
