from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import POSTGRES_URL, bot, Director
from db.utils import get_product_from_category, get_product_photos

import asyncpg
import buttons


# =======================================================================================================================

class all_products_director_fsm(StatesGroup):
    category = State()


async def fsm_start(message: types.Message):
    if message.from_user.id in Director:
        await all_products_director_fsm.category.set()
        await message.answer(f"Категория товара?", reply_markup=buttons.CategoryButtonsDirector)
    else:
        await message.answer('Вы не директор!')


"""Вывод категорий"""
async def load_category(message: types.Message, state: FSMContext):
    if message.from_user.id in Director:
        category = message.text.replace("/", "")
        pool = await asyncpg.create_pool(POSTGRES_URL)
        products = await get_product_from_category(pool, category)

        if products:
            for product in products:
                # Отправка информации о товаре
                product_info = (
                    f"Информация: {product['info']}\n"
                    f"Категория: {product['category']}\n"
                    f"Артикул: {product['article_number']}\n"
                    f"Количество: {product['quantity']}\n"
                    f"Цена: {product['price']}"
                )

                # Получение и отправка фотографий товара
                photos = await get_product_photos(pool, product['id'])
                photo_urls = [photo['photo'] for photo in photos]

                media_group = [types.InputMediaPhoto(media=image) for image in photo_urls[:-1]]

                last_image = photo_urls[-1]
                last_media = types.InputMediaPhoto(media=last_image, caption=product_info)

                media_group.append(last_media)

                await bot.send_media_group(chat_id=message.chat.id,
                                           media=media_group)

        else:
            await message.answer("В выбранной категории нет товаров")
    else:
        await message.answer('Вы не директор!')


async def cancel_reg(message: types.Message, state: FSMContext):
    if message.from_user.id in Director:
        current_state = await state.get_state()
        if current_state is not None:
            await state.finish()
            await message.answer('Отменено!', reply_markup=buttons.StartDirector)
    else:
        await message.answer('Вы не директор!')


# =======================================================================================================================
def register_all_products_director(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals="Сancel", ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands=["Товары", 'all_products_director'])
    dp.register_message_handler(load_category, state=all_products_director_fsm.category)