from aiogram import types, Dispatcher
from config import POSTGRES_URL, bot, Director
from db.utils import get_product_from_category, get_product_photos
from db.ORM import delete_product
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

import asyncpg
import buttons


# =======================================================================================================================
async def fsm_start(message: types.Message):
    if message.from_user.id in Director:
        category_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
        commands = ["/Обувь", "/Нижнее_белье", "/Акссесуары", "/Верхняя_одежда", "/Штаны", "/Отмена🚫"]

        buttons_row1 = [KeyboardButton(command) for command in commands[:len(commands)//3]]
        buttons_row2 = [KeyboardButton(command) for command in commands[len(commands)//3:]]

        category_buttons.add(*buttons_row1)
        category_buttons.add(*buttons_row2)

        await message.answer("Выберите категорию товара:", reply_markup=category_buttons)
    else:
        await message.answer('Вы не директор!')


"""Вывод категорий"""
async def load_category(message: types.Message, category: str):
    if message.from_user.id in Director:
        pool = await asyncpg.create_pool(POSTGRES_URL)
        products = await get_product_from_category(pool, category)

        if products:
            for product in products:
                if product["category"] == category:
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
        else:
            await message.answer("В выбранной категории нет товаров")
    else:
        await message.answer('Вы не директор!')


async def all_products_shoes(message: types.Message):
    category = message.text.replace("/", "")
    await load_category(message, category)

async def all_products_outerwear(message: types.Message):
    category = message.text.replace("/", "")
    await load_category(message, category)

async def all_products_underwear(message: types.Message):
    category = message.text.replace("/", "")
    await load_category(message, category)

async def all_products_accessories(message: types.Message):
    category = message.text.replace("/", "")
    await load_category(message, category)

async def all_products_trousers(message: types.Message):
    category = message.text.replace("/", "")
    await load_category(message, category)


async def complete_delete_product(call: types.CallbackQuery):
    product_id = call.data.replace("delete_product", "").strip()
    await delete_product(product_id)
    await call.message.reply(text="Удалено из базы данных")



async def cancel_reg(message: types.Message):
    if message.from_user.id in Director:
        await message.answer('Отменено!', reply_markup=buttons.StartDirector)
    else:
        await message.answer('Вы не директор!')

# =======================================================================================================================
def register_all_products_director(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, commands=["Отмена🚫", 'all_products_director'])
    dp.register_message_handler(fsm_start, commands=["Товары*", 'all_products_director'])
    dp.register_message_handler(all_products_shoes, commands=["Обувь", 'all_products_director'])
    dp.register_message_handler(all_products_accessories, commands=["Акссесуары", 'all_products_director'])
    dp.register_message_handler(all_products_outerwear, commands=["Верхняя_одежда", 'all_products_director'])
    dp.register_message_handler(all_products_underwear, commands=["Нижнее_белье", 'all_products_director'])
    dp.register_message_handler(all_products_trousers, commands=["Штаны", 'all_products_director'])
    dp.register_callback_query_handler(complete_delete_product,
                                       lambda call: call.data and call.data.startswith("delete_product"))
