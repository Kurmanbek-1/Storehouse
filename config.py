from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from decouple import config

storage = MemoryStorage()

TOKEN = config("TOKEN")

Admins = [6451475162, ]

Director = [6451475162, ]
bot = Bot(TOKEN)

dp = Dispatcher(bot=bot, storage=storage)