from typing import Union

from aiogram.types import Message, CallbackQuery

from loader import db
from utils.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'

    user_id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(50), nullable=True)
    name = db.Column(db.String(400))


class UserFunction:
    db = User

    async def get_user_by_tg_id(self, tg_id: int):
        print(tg_id)
        return await self.db.query.where(self.db.user_id == tg_id).gino.first()

    async def create_user_by_message(self, message: Union[Message, CallbackQuery]):
        if isinstance(message, CallbackQuery):
            message = message.message

        await self.db(
            user_id=message.from_user.id,
            username=message.from_user.username,
            name=message.from_user.full_name,
        ).create()

    async def update_user_info_by_message(self, message: Message):
        user = await self.db().get(message.from_user.id)
        if user:
            await user.update(
                username=message.from_user.username, name=message.from_user.full_name
            ).apply()
