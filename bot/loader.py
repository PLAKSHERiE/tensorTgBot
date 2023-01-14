from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from gino import Gino

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
# storage = MemoryStorage()
storage = RedisStorage2(host=config.REDIS_HOST, port=config.REDIS_PORT)

dp = Dispatcher(bot, storage=storage)
db = Gino()
