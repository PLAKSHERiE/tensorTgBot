import datetime
import logging

import pytz
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data import config
from services.apscheduller.history_billing import get_history_billing
from utils.db_api.schemas.account_function import AccountFunction

logging.basicConfig()
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)

DEFAULT = "default"

jobstores = {
    DEFAULT: RedisJobStore(
        db=config.REDIS_DB_JOBSTORE,
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        jobs_key='dispatched_notifications_jobs',
        run_times_key='dispatched_notifications_running'
    )
}
executors = {DEFAULT: AsyncIOExecutor()}
# scheduler = AsyncIOScheduler(jobstores=jobstores, executors=executors, timezone=utc)
scheduler = AsyncIOScheduler(jobstores=jobstores, executors=executors, timezone="Europe/Moscow")
background_scheduler = AsyncIOScheduler(jobstores=jobstores, executors=executors, timezone="Europe/Moscow")


async def init_jobs():
    logging.info("Clear jobs")
    await AccountFunction().reset_update_data()
    scheduler.print_jobs()
    scheduler.remove_all_jobs()
    scheduler.add_job(check_history_billing, 'interval', seconds=10, coalesce=True)
    scheduler.print_jobs()
    scheduler.resume()


async def on_startup_scheduler():
    logging.info("Setup Scheduler")
    scheduler.start(paused=True)


async def on_shutdown_scheduler():
    scheduler.shutdown()


async def check_history_billing():
    accounts = await AccountFunction().get_active_accounts()
    # print(accounts)
    for account in accounts:
        if account.update_billing:
            continue
        if datetime.datetime.now(pytz.utc) < account.last_update_billing + \
                datetime.timedelta(minutes=account.period_update):
            continue
        await AccountFunction().edit_account_field(account.id, 'update_billing', True)
        args = {
            'login': account.login,
            'password': account.password,
            'token': account.token,
            'user_id': account.user,
            'id': account.id,
            'data_display': account.data_display
        }
        scheduler.add_job(get_history_billing, trigger='date', misfire_grace_time=None,
                          run_date=datetime.datetime.now(), args=[args])
