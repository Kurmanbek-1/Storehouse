from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()

TOKEN = "6941198906:AAFT-FnZPOWX3JhMtk9nzO8GS_9f_joZadI"

Admins = [995712956, ]

Director = [995712956, ]
bot = Bot(TOKEN)

dp = Dispatcher(bot=bot, storage=storage)
