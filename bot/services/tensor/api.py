import asyncio
import json
import logging
import datetime
from typing import Tuple, Union

import aiohttp


class TensorAPI:
    METHOD_AUTH = 'САП.Аутентифицировать'
    METHOD_HISTORY = 'Billing.GetHistory'

    URL_AUTH = 'https://fix-reg.tensor.ru/auth/service/'
    URL_API = 'https://fix-reg.tensor.ru/partner_api/service/'

    ERROR_AUTH_TEXT = 'Ошибка в авторизации. '
    ERROR_AUTH_NO_VALID_TEXT = 'Проверьте правильность ввода логина и пароля.'
    ERROR_AUTH = None

    def __init__(self, login: str, password: str, token: Union[str, None] = None):
        self.LOGIN = login
        self.PASSWORD = password
        self.TOKEN = token

    def get_headers(self, type_: str = None) -> dict:
        headers = {
            'Host': 'fix-reg.tensor.ru',
            'Content-Type': 'application/json-rpc; charset=utf-8',
            'Accept': 'application/json-rpc'
        }
        if type_ == 'api':
            headers['X-SBISSessionID'] = self.TOKEN
        return headers

    @staticmethod
    def get_body(method: str, params: dict) -> Tuple[int, dict]:
        id_ = 1
        body = {
            "jsonrpc": "2.0",
            "protocol": 2,
            "id": id_,
            "method": method,
            "params": params,
        }
        return id_, body

    async def auth(self) -> str:
        self.ERROR_AUTH = None
        id_, body = self.get_body(self.METHOD_AUTH, {'login': self.LOGIN, 'password': self.PASSWORD})
        headers = self.get_headers()
        result = None

        while result is None:
            async with aiohttp.ClientSession(trust_env=True) as session:
                async with session.post(self.URL_AUTH,
                                        data=json.dumps(body),
                                        headers=headers,
                                        ssl=False,
                                        timeout=50) as r:
                    try:
                        data = await r.json()
                        if 'error' in data:
                            result = self.ERROR_AUTH_TEXT + data['error']['details']
                            self.ERROR_AUTH = data['error']['details']
                        else:
                            result = data['result']
                            self.TOKEN = result
                    except Exception as e:
                        logging.error(f'Ошибка в авторизации {e}')
                        result = self.ERROR_AUTH_TEXT
                        self.ERROR_AUTH = self.ERROR_AUTH_TEXT
                    await asyncio.sleep(0.2)

        return result

    async def history_api(self) -> dict:
        id_, body = self.get_body(self.METHOD_HISTORY, {
            'DateFrom': datetime.date.today().strftime('%Y-%m-%d'),
            'DateTo': datetime.date.today().strftime('%Y-%m-%d'),
            # 'DateFrom': '2022-12-01',
            # 'DateTo': '2023-01-11',
            'PointSale': None,
            'SubPoints': False,
            'NavigationKey': None,
        })
        result = await self.api(body)
        return result

    async def api(self, body: dict) -> dict:
        self.ERROR_AUTH = None
        result = None

        while result is None:
            headers = self.get_headers(type_='api')
            async with aiohttp.ClientSession(trust_env=True) as session:
                async with session.post(self.URL_API,
                                        data=json.dumps(body),
                                        headers=headers,
                                        ssl=False,
                                        timeout=50) as r:
                    try:
                        if r.status == 401:
                            await asyncio.sleep(2)
                            await self.auth()
                            if self.ERROR_AUTH:
                                result = {
                                    'error': {
                                        'details': self.ERROR_AUTH
                                    }
                                }
                        elif r.status != 200:
                            error = f'статус запроса {r.status}'
                            logging.error(f'ОШИБКА ОТ СЕРВЕРА: {error}')
                            result = {
                                'error': {
                                    'details': f'Ошибка от сервера - {error}'
                                }
                            }
                        else:
                            result = await r.json()
                    except Exception as e:
                        logging.error(e)
                        result = {}
                    await asyncio.sleep(1)

        return result


async def test():
    api = TensorAPI('petr-test', 'petr-test*12')
    await api.auth()
    print(api.TOKEN)
    print(api.ERROR_AUTH)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test())
