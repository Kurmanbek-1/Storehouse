from aiogram.utils import executor
import logging
from config import dp, bot, Admins
from keyboards import buttons


# ===========================================================================
async def on_startup(_):
    for i in Admins:
        await bot.send_message(chat_id=i, text="Бот запущен!", reply_markup=buttons.start_admins_markup)


# ===========================================================================
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
