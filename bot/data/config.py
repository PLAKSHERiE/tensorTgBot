from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")

POSTGRES_USER = env.str("DB_LOGIN")
POSTGRES_PASSWORD = env.str("DB_PASS")
POSTGRES_HOST = env.str("DB_HOST")
POSTGRES_DB = env.str("DB_NAME")
POSTGRES_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"

REDIS_HOST = env.str("REDIS_HOST")
REDIS_PORT = env.str("REDIS_PORT")
REDIS_DB_JOBSTORE = env.int("REDIS_DB_JOBSTORE")
