from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()

TOKEN = ""

Admins = [995712956, ]

Director = [995712956, ]
bot = Bot(TOKEN)

dp = Dispatcher(bot=bot, storage=storage)



