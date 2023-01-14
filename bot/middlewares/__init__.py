from aiogram import Dispatcher
from loguru import logger

from loader import dp
from .acl import ACLMiddleware
from .throttling import ThrottlingMiddleware


if __name__ == "middlewares":
    logger.info("Configure middlewares...")
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(ACLMiddleware())
