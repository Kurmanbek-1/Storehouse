from aiogram.utils import executor
import logging
from config import dp, bot, Admins, data_base

from handlers import commands, reviews
from handlers.FSM_for_client import pre_order, Order_for_client, all_products, \
    all_pre_orders, review_client
from handlers.FSM_for_admins import pre_order_for_admins, fill_products
import buttons

from db.ORM import create_tables


# ===========================================================================
async def on_startup(_):
    for i in Admins:
        await bot.send_message(chat_id=i, text="Бот запущен!", reply_markup=buttons.StartAdmin)
    await data_base.connect()
    await create_tables()


async def on_shutdown(_):
    await data_base.close()


commands.register_commands(dp)
pre_order.register_pre_order(dp)
pre_order_for_admins.register_pre_order_for_admins(dp)
Order_for_client.register_order_for_client(dp)
fill_products.register_fill_products(dp)
all_products.register_all_products(dp)
all_pre_orders.register_all_preorders(dp)
review_client.register_review(dp)
reviews.register_all_reviews_for_directors(dp)

# ===========================================================================
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)