from aiogram.utils import executor
import logging
from config import dp, bot, Admins

from handlers import commands
from handlers.FSM import pre_order


# ===========================================================================
async def on_startup(_):
    for i in Admins:
        await bot.send_message(chat_id=i, text="Бот запущен!", reply_markup=None)

commands.register_commands(dp)
pre_order.register_pre_order(dp)

# ===========================================================================
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

