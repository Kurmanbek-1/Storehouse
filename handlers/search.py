from aiogram import types, Dispatcher
from config import POSTGRES_URL, bot, Admins, Director
from db.utils import get_product_from_article, get_product_photos
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

import asyncpg
import buttons

class all_products_from_article_fsm(StatesGroup):
    article = State()

async def fsm_start_search(message: types.Message):
    await all_products_from_article_fsm.article.set()
    await message.answer("Введите артикул товара!", reply_markup=buttons.CancelSearch)

async def search_article(message: types.Message):
    pool = await asyncpg.create_pool(POSTGRES_URL)
    article_number = message.text
    products = await get_product_from_article(pool, article_number)

    if products:
        for product in products:
            if product["article_number"] == article_number:
                product_info = (
                    f"Информация: {product['info']}\n"
                    f"Категория: {product['category']}\n"
                    f"Артикул: {product['article_number']}\n"
                    f"Количество: {product['quantity']}\n"
                    f"Цена: {product['price']}"
                )

                photos = await get_product_photos(pool, product['id'])
                photo_urls = [photo['photo'] for photo in photos]

                media_group = [types.InputMediaPhoto(media=image) for image in photo_urls[:-1]]

                last_image = photo_urls[-1]
                last_media = types.InputMediaPhoto(media=last_image, caption=product_info)

                media_group.append(last_media)

                await bot.send_media_group(chat_id=message.chat.id,
                                           media=media_group)
    else:
        await message.answer("Товаров с данным артиклем не существует!", reply_markup=buttons.CancelSearch)

async def cancel_search(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        if message.from_user.id in Admins:
            await state.finish()
            await message.answer('Отменено!', reply_markup=buttons.StartAdmin)
        elif message.from_user.id in Director:
            await state.finish()
            await message.answer('Отменено!', reply_markup=buttons.StartDirector)
        else:
            await state.finish()
            await message.answer('Отменено!', reply_markup=buttons.StartClient)


def register_search(dp: Dispatcher):
    dp.register_message_handler(cancel_search, Text(equals="/Выход из поиска🚫", ignore_case=True), state="*")
    dp.register_message_handler(fsm_start_search, commands=["Поиск", 'search'])
    dp.register_message_handler(search_article, state=all_products_from_article_fsm.article)