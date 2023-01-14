from typing import Any, Tuple, Union

from aiogram.types import CallbackQuery

from services.tensor.api import TensorAPI
from utils.db_api.schemas.account import Account
from utils.db_api.schemas.user import User


class AccountFunction:
    db = Account
    db_user = User
    tensor_api = TensorAPI

    async def get_all_accounts_by_user_id(self, user_id: int):
        user = await self.db_user().get(user_id)
        return await self.db.query.where(self.db.user == user.user_id).gino.all()

    async def get_account_by_id(self, account_id: int):
        return await self.db().get(account_id)

    async def create_account(self, message: CallbackQuery, data: dict, token: str):
        user = await self.db_user().get(message.from_user.id)
        await self.db(
            user=user.user_id,
            login=data['login'],
            password=data['password'],
            token=token,
            period_update=data['period_update'],
            data_display=data['data_display'],
        ).create()

    async def edit_account_field(self, account_id: int, field: str, value: Any):
        account = await self.db().get(account_id)
        await account.update(**{field: value}).apply()

    async def delete_account(self, account_id: int):
        account = await self.db().get(account_id)
        await account.delete()

    async def check_valid_account(self, account_id: int) -> Tuple[bool, Union[None, str]]:
        valid = True
        error = None
        account = await self.db().get(account_id)
        api = self.tensor_api(account.login, account.password)
        await api.auth()
        if api.ERROR_AUTH:
            valid = False
            error = api.ERROR_AUTH
            await account.update(correct=False).apply()
        else:
            await account.update(correct=True, token=api.TOKEN).apply()

        return valid, error

    async def get_active_accounts(self) -> list:
        return await self.db.query.where(self.db.active.is_(True)).where(self.db.correct.is_(True)).gino.all()

    async def reset_update_data(self):
        await self.db.update.values(update_billing=False).where(self.db.update_billing.is_(True)).gino.status()

    async def check_account_exist(self, user_id: int, login: str) -> bool:
        account = await self.db.query.where(self.db.user == user_id).where(self.db.login == login).gino.all()
        return len(account) > 0
