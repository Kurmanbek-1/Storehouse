# import asyncpg
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

import os
import buttons


# async def get_conn():
#     conn = await asyncpg.connect(user='postgres', password='123',
#                                  database='osor_tg_bot', host='localhost')
#     return conn


# =======================================================================================================================

class all_products_fsm(StatesGroup):
    city = State()
    category = State()


async def fsm_start(message: types.Message):
    await all_products_fsm.city.set()
    await message.answer("Выберите город:", reply_markup=buttons.city_markup)


async def choose_city(message: types.Message, state: FSMContext):
    selected_city = message.text
    await state.update_data(city=selected_city)
    await all_products_fsm.category.set()
    await message.answer(f"Категория товара для города {selected_city}?", reply_markup=buttons.all_categories)


"""Вывод категорий"""


async def load_category(message: types.Message, state: FSMContext):
    category_name = message.text
    data = await state.get_data()
    city = data.get("city")

    try:
        conn = await get_conn()
        categories = await conn.fetch(
            "SELECT * FROM products_coming WHERE category = $1 AND city = $2",
            category_name, city)
    except Exception as e:
        await message.answer(f"Ошибка SQL-запроса: {e}")
        return
    finally:
        await conn.close()

    if not categories:
        await message.answer(f"Категория '{category_name}' в городе '{city}' не найдена.")
        return

    for category in categories:
        photo_path = category[9]

        if not os.path.exists(photo_path):
            print(f"Файл не найден: {photo_path}")
            continue
        try:
            with open(photo_path, 'rb') as photo:
                await message.answer_photo(photo=photo, caption=f"Товар: {category[1]}\n"
                                                                f"Информация о товаре: {category[2]}\n"
                                                                f"Цена: {category[4]}\n"
                                                                f"Город: {category[5]}\n"
                                                                f"Категория: {category[6]}\n"
                                                                f"Артикул: {category[7]}\n",
                                           reply_markup=buttons.start)
                await state.finish()
        except Exception as e:
            print(f"Ошибка при открытии файла {photo_path}: {e}")
            continue


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=buttons.start)


# =======================================================================================================================
def register_all_products(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals="/cancel", ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands=["Товары!", 'all_products'])
    dp.register_message_handler(choose_city, state=all_products_fsm.city)
    dp.register_message_handler(load_category, state=all_products_fsm.category)
