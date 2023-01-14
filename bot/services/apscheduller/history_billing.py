import datetime
import logging

import emoji
import pytz

from loader import bot
from services.tensor.api import TensorAPI
from utils.db_api.schemas.account_function import AccountFunction
from utils.db_api.schemas.user import UserFunction

ERROR_API = f'{emoji.emojize(":red_exclamation_mark:")} <b>Ошибка обновления API:</b>'


async def get_history_billing(account: dict):
    """
    Проверяет историю аккаунта
    :param account: Данные аккаунта
    :return:
    """
    try:
        api = TensorAPI(account['login'], account['password'], account['token'])
        history = await api.history_api()
        # logging.info(history)
        user = await UserFunction().get_user_by_tg_id(account['user_id'])
        """
        Обработка ошибок
        """
        if 'error' in history:
            if api.ERROR_AUTH_NO_VALID_TEXT in history['error']['details']:
                await bot.send_message(user.user_id, f"{ERROR_API} <code>{history['error']['details']}</code>")
                await AccountFunction().edit_account_field(account['id'], 'correct', False)
            else:
                await bot.send_message(user.user_id, f"{ERROR_API} <code>{history['error']['details']}</code>")
            # await AccountFunction().edit_account_field(account['id'], 'correct', False)
            await AccountFunction().edit_account_field(account['id'], 'update_billing', False)
            return
        """
        Обработка элементов
        """
        await AccountFunction().edit_account_field(account['id'], 'token', api.TOKEN)
        if 'result' in history:
            keys = {}
            filtered_items = []
            for index, key in enumerate(history['result']['s']):
                keys[key['n']] = index
            for item in history['result']['d']:
                if item[keys['Action']] in account['data_display']:
                    filtered_items.append(item)
            if filtered_items:
                filtered_items_string = ''
                for item in filtered_items:
                    filtered_items_string += f'{item}\n'
                await bot.send_message(user.user_id, filtered_items_string)

    except Exception as e:
        logging.error(e)
    finally:
        await AccountFunction().edit_account_field(account['id'], 'update_billing', False)
        await AccountFunction().edit_account_field(account['id'], 'last_update_billing',
                                                   datetime.datetime.now(pytz.utc))


if __name__ == '__main__':
    date = datetime.datetime.today()
    print(date.strftime('%Y-%m-%d'))
