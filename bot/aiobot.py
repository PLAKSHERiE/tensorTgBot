from aiogram import executor
import logging

from loader import dp
import middlewares
import filters
import handlers
from services.apscheduller.apscheduller import on_startup_scheduler, init_jobs
from utils.db_api.db_gino import on_startup_gino
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from aiogram.contrib.middlewares.logging import LoggingMiddleware

logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())
logging.getLogger('gino.engine._SAEngine').setLevel(logging.ERROR)


async def on_startup(dispatcher):
    # БД
    await on_startup_gino()
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)
    # Scheduler
    await on_startup_scheduler()
    # Scheduler clear
    await init_jobs()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
