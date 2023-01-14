from typing import Optional, Tuple, Union

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from utils.db_api.schemas.user import User, UserFunction


class ACLMiddleware(BaseMiddleware):
    async def setup_chat(self, message: Union[Message, CallbackQuery], data: dict, user: types.User,
                         chat: Optional[types.Chat] = None):
        user_id = user.id
        chat_id = chat.id if chat else user.id
        chat_type = chat.type if chat else "private"
        # if isinstance(message, CallbackQuery):
        #     message = message.message

        user = await User.get(user_id)
        if user is None:
            user = await UserFunction().create_user_by_message(message=message)
        else:
            if user.username != message.from_user.username or user.name != message.from_user.full_name:
                await UserFunction().update_user_info_by_message(message)

        data["user"] = user
        data["chat"] = chat

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(message, data, message.from_user, message.chat)

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        await self.setup_chat(query, data, query.from_user, query.message.chat if query.message else None)
