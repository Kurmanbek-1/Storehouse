from aiogram.utils import executor
import logging
from config import dp, bot, Admins

from handlers import commands
from handlers.FSM_for_client import pre_order, Order_for_client
from handlers.FSM_for_admins import pre_order_for_admins, fill_products
import buttons


# ===========================================================================
async def on_startup(_):
    for i in Admins:
        await bot.send_message(chat_id=i, text="Бот запущен!", reply_markup=buttons.StartAdmin)


commands.register_commands(dp)
pre_order.register_pre_order(dp)
pre_order_for_admins.register_pre_order_for_admins(dp)
Order_for_client.register_order_for_client(dp)
fill_products.register_fill_products(dp)

# ===========================================================================
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)