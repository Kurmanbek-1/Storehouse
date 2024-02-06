from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from decouple import config
from db.db_storehouse import Database


storage = MemoryStorage()

TOKEN = config('TOKEN')


Director = [6451475162, 1738805992, ]

Admins = [995712956, 1000541805, 958938518, 6127093234, ]

Developers = [995712956, ]

bot = Bot(TOKEN)

dp = Dispatcher(bot=bot, storage=storage)

ip = config('ip')
PostgresUser = config('PostgresUser')
PostgresPassword = config('PostgresPassword')
DATABASE = config('DATABASE')

POSTGRES_URL = f"postgresql://{PostgresUser}:{PostgresPassword}@{ip}/{DATABASE}"

data_base = Database(POSTGRES_URL)