from aiogram import types, Dispatcher
from config import POSTGRES_URL, bot, Director
from db.utils import get_product_from_category, get_product_photos
from db.ORM import delete_product
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
import asyncpg
import buttons

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

# =======================================================================================================================
class all_products_director_fsm(StatesGroup):
    category = State()
    more_tovars = State()


async def fsm_start(message: types.Message):
    if message.from_user.id in Director:
        await all_products_director_fsm.category.set()
        await message.answer(f"Категория товара?", reply_markup=buttons.CategoryButtonsDirector)
    else:
        await message.answer('Вы не админ!')


"""Вывод категорий"""
async def load_category(message: types.Message, state: FSMContext):
    if message.from_user.id in Director:
        if message.text.startswith("/"):
            category = message.text.replace("/", "")
            pool = await asyncpg.create_pool(POSTGRES_URL)
            products = await get_product_from_category(pool, category)

            if products:
                if len(products) <= 5:
                    for product in products:
                        product_info = (
                            f"Информация: {product['info']}\n"
                            f"Категория: {product['category']}\n"
                            f"Артикул: {product['article_number']}\n"
                            f"Количество: {product['quantity']}\n"
                            f"Цена: {product['price']}"
                        )

                        keyboard = InlineKeyboardMarkup().add(
                            InlineKeyboardButton(
                                f"Удалить",
                                callback_data=f"delete_product{product['id']}"
                            )
                        )

                        photos = await get_product_photos(pool, product['id'])
                        photo_urls = [photo['photo'] for photo in photos]
                        media_group = [types.InputMediaPhoto(media=image) for image in photo_urls]

                        await bot.send_media_group(chat_id=message.chat.id, media=media_group)
                        await bot.send_message(chat_id=message.chat.id, text=product_info, reply_markup=keyboard)

                    await state.finish()
                    await message.answer(f"Это все товары из категории: {category}",
                                         reply_markup=buttons.StartDirector)
                    await message.answer("Чтобы удалить товар нажмите на кнопку 'Удалить' под сообщением")
                else:
                    chunks = [products[i:i + 5] for i in range(0, len(products), 5)]
                    data = await state.get_data()
                    current_chunk = data.get("current_chunk", 0)
                    current_products = chunks[current_chunk]

                    for product in current_products:
                        product_info = (
                            f"Информация: {product['info']}\n"
                            f"Категория: {product['category']}\n"
                            f"Артикул: {product['article_number']}\n"
                            f"Количество: {product['quantity']}\n"
                            f"Цена: {product['price']}"
                        )

                        keyboard = InlineKeyboardMarkup().add(
                            InlineKeyboardButton(
                                f"Удалить",
                                callback_data=f"delete_product{product['id']}"
                            )
                        )

                        photos = await get_product_photos(pool, product['id'])
                        photo_urls = [photo['photo'] for photo in photos]
                        media_group = [types.InputMediaPhoto(media=image) for image in photo_urls]

                        await bot.send_media_group(chat_id=message.chat.id, media=media_group)
                        await bot.send_message(chat_id=message.chat.id, text=product_info, reply_markup=keyboard)

                    await state.update_data(current_chunk=current_chunk + 1)

                    if current_chunk < len(chunks) - 1:
                        ShowMore = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
                        ShowMore.add(KeyboardButton(f'Ещё из категории: {category}'))
                        ShowMore.add(KeyboardButton('/Отмена🚫'))
                        await message.answer("Показать еще?", reply_markup=ShowMore)
                        await message.answer("Чтобы удалить товар, нажмите на кнопку (/Отмена🚫), "
                                             "либо выведите все товары до конца!")
                        await all_products_director_fsm.next()
            else:
                await message.answer("В выбранной категории нет товаров")
        else:
            category = message.text.split()[-1]
            pool = await asyncpg.create_pool(POSTGRES_URL)
            products = await get_product_from_category(pool, category)

            if products:
                chunks = [products[i:i + 5] for i in range(0, len(products), 5)]
                data = await state.get_data()
                current_chunk = data.get("current_chunk", 0)
                current_products = chunks[current_chunk]

                for product in current_products:
                    product_info = (
                        f"Информация: {product['info']}\n"
                        f"Категория: {product['category']}\n"
                        f"Артикул: {product['article_number']}\n"
                        f"Количество: {product['quantity']}\n"
                        f"Цена: {product['price']}"
                    )

                    keyboard = InlineKeyboardMarkup().add(
                        InlineKeyboardButton(
                            f"Удалить",
                            callback_data=f"delete_product{product['id']}"
                        )
                    )

                    photos = await get_product_photos(pool, product['id'])
                    photo_urls = [photo['photo'] for photo in photos]
                    media_group = [types.InputMediaPhoto(media=image) for image in photo_urls]

                    await bot.send_media_group(chat_id=message.chat.id, media=media_group)
                    await bot.send_message(chat_id=message.chat.id, text=product_info, reply_markup=keyboard)

                await state.update_data(current_chunk=current_chunk + 1)

                if current_chunk < len(chunks) - 1:
                    ShowMore = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
                    ShowMore.add(KeyboardButton(f'Ещё из категории: {category}'))
                    ShowMore.add(KeyboardButton('/Отмена🚫'))
                    await message.answer("Показать еще?", reply_markup=ShowMore)
                    await message.answer("Чтобы удалить товар, нажмите на кнопку (/Отмена🚫), "
                                         "либо выведите все товары до конца!")
                    await all_products_director_fsm.more_tovars.set()
                else:
                    await state.finish()
                    await message.answer(f"Это все товары из категории: {category}",
                                         reply_markup=buttons.StartDirector)
                    await message.answer("Чтобы удалить товар нажмите на кнопку 'Удалить' под сообщением")
            else:
                await message.answer("В выбранной категории нет товаров")

    else:
        await message.answer('Вы не директор!')

async def complete_delete_product(call: types.CallbackQuery):
    product_id = call.data.replace("delete_product", "").strip()
    await delete_product(product_id)
    await call.message.reply(text="Удалено из базы данных")


async def load_more(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await load_category(message, state)


async def cancel_reg(message: types.Message, state: FSMContext):
    if message.from_user.id in Director:
        current_state = await state.get_state()
        if current_state is not None:
            await state.finish()
            await message.answer('Отменено!', reply_markup=buttons.StartDirector)
            await message.answer("Чтобы удалить товар нажмите на кнопку 'Удалить' под сообщением")
    else:
        await message.answer('Вы не директор!')

# =======================================================================================================================
def register_all_products_director(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals="/Отмена🚫", ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands=["Товары*", 'all_products_director'])
    dp.register_message_handler(load_category, state=all_products_director_fsm.category)
    for category in ["Обувь", "Нижнее_белье", "Акссесуары", "Верхняя_одежда", "Штаны"]:
        dp.register_message_handler(load_more, Text(equals=f"Ещё из категории: {category}", ignore_case=True),
                                    state=all_products_director_fsm.more_tovars)
    dp.register_callback_query_handler(complete_delete_product,
                                       lambda call: call.data and call.data.startswith("delete_product"))
