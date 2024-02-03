from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import POSTGRES_URL, bot, Admins
from db.utils import get_product_from_category, get_product_photos

import asyncpg
import buttons


# =======================================================================================================================

class all_products_admin_fsm(StatesGroup):
    category = State()
    more_tovars = State()


async def fsm_start(message: types.Message):
    if message.from_user.id in Admins:
        await all_products_admin_fsm.category.set()
        await message.answer(f"Категория товара?", reply_markup=buttons.CategoryButtonsAdmins)
    else:
        await message.answer('Вы не админ!')


"""Вывод категорий"""
async def load_category(message: types.Message, state: FSMContext):
    if message.from_user.id in Admins:
        current_state = await state.get_state()
        if current_state is not None:
            category = message.text.replace("/", "")
            pool = await asyncpg.create_pool(POSTGRES_URL)
            products = await get_product_from_category(pool, category)

            if products:
                # Разбиваем товары на порции по 7 штук
                chunks = [products[i:i + 7] for i in range(0, len(products), 7)]

                # Получаем текущую порцию товаров
                data = await state.get_data()
                current_chunk = data.get("current_chunk", 0)
                current_products = chunks[current_chunk]

                for product in current_products:
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

                    await bot.send_media_group(chat_id=message.chat.id, media=media_group)

                # Устанавливаем в состояние номер следующей порции товаров
                await state.update_data(current_chunk=current_chunk + 1)

                # Если еще остались порции товаров, добавляем кнопку "Далее"
                if current_chunk < len(chunks) - 1:
                    await message.answer("Показать еще?", reply_markup=buttons.ShowMore)
                    await all_products_admin_fsm.next()
            else:
                await message.answer("В выбранной категории нет товаров")

async def load_more(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await load_category(message, state)


async def cancel_reg(message: types.Message, state: FSMContext):
    if message.from_user.id in Admins:
        current_state = await state.get_state()
        if current_state is not None:
            await state.finish()
            await message.answer('Отменено!', reply_markup=buttons.StartAdmin)
    else:
        await message.answer('Вы не админ!')


# =======================================================================================================================
def register_all_products_admins(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals="Отмена!", ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands=["Заказы", 'all_products_admins'])
    dp.register_message_handler(load_category, state=all_products_admin_fsm.category)
    dp.register_message_handler(load_more, Text(equals="Далее", ignore_case=True), state=all_products_admin_fsm.more_tovars)