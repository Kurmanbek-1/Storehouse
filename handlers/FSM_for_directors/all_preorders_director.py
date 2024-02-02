from aiogram import types, Dispatcher
from config import POSTGRES_URL, bot, Director
from db.utils import get_preorder_from_category, get_preorder_photos
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from db.ORM import delete_preorder

import asyncpg
import buttons


# =======================================================================================================================
async def fsm_start(message: types.Message):
    if message.from_user.id in Director:
        category_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
        commands = ["/Обувь/", "/Нижнее_белье/", "/Акссесуары/", "/Верхняя_одежда/", "/Штаны/", "/Отмена🚫"]

        buttons_row1 = [KeyboardButton(command) for command in commands[:len(commands)//3]]
        buttons_row2 = [KeyboardButton(command) for command in commands[len(commands)//3:]]

        category_buttons.add(*buttons_row1)
        category_buttons.add(*buttons_row2)

        await message.answer("Выберите категорию предзаказа:", reply_markup=category_buttons)
    else:
        await message.answer('Вы не директор!')


async def load_preorder_category(message: types.Message, category: str):
    if message.from_user.id in Director:
        pool = await asyncpg.create_pool(POSTGRES_URL)
        preorders = await get_preorder_from_category(pool, category)

        if preorders:
            for preorder in preorders:
                if preorder["category"] == category:
                    preorder_info = (
                        f"Информация: {preorder['info']}\n"
                        f"Категория: {preorder['category']}\n"
                        f"Артикул: {preorder['preorder_article']}\n"
                        f"Количество: {preorder['quantity']}\n"
                        f"Дата выхода: {preorder['product_release_date']}\n"
                        f"Цена: {preorder['price']}"
                    )

                    keyboard = InlineKeyboardMarkup().add(
                        InlineKeyboardButton(
                            f"Удалить",
                            callback_data=f"delete_preorder{preorder['id']}"
                        )
                    )

                    photos = await get_preorder_photos(pool, preorder['id'])
                    photo_urls = [photo['photo'] for photo in photos]
                    media_group = [types.InputMediaPhoto(media=image) for image in photo_urls]

                    await bot.send_media_group(chat_id=message.chat.id, media=media_group)
                    await bot.send_message(chat_id=message.chat.id, text=preorder_info, reply_markup=keyboard)
        else:
            await message.answer("В выбранной категории нет предзаказов")
    else:
        await message.answer('Вы не директор!')


async def all_preorders_shoes(message: types.Message):
    category = message.text.replace("/", "")
    await load_preorder_category(message, category)

async def all_preorders_outerwear(message: types.Message):
    category = message.text.replace("/", "")
    await load_preorder_category(message, category)

async def all_preorders_underwear(message: types.Message):
    category = message.text.replace("/", "")
    await load_preorder_category(message, category)

async def all_preorders_accessories(message: types.Message):
    category = message.text.replace("/", "")
    await load_preorder_category(message, category)

async def all_preorders_trousers(message: types.Message):
    category = message.text.replace("/", "")
    await load_preorder_category(message, category)


async def complete_delete_preorder(call: types.CallbackQuery):
    preorder_id = call.data.replace("delete_preorder", "").strip()
    await delete_preorder(preorder_id)
    await call.message.reply(text="Удалено из базы данных")


async def cancel_reg(message: types.Message):
    if message.from_user.id in Director:
        await message.answer('Отменено!', reply_markup=buttons.StartDirector)
    else:
        await message.answer('Вы не директор!')

# =======================================================================================================================
def register_all_preorders_director(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, commands=["Отмена🚫", 'all_preorders_director'])
    dp.register_message_handler(fsm_start, commands=["Предзаказы*", 'all_preorders_director'])
    dp.register_message_handler(all_preorders_shoes, commands=["Обувь/", 'all_preorders_director'])
    dp.register_message_handler(all_preorders_accessories, commands=["Акссесуары/", 'all_preorders_director'])
    dp.register_message_handler(all_preorders_outerwear, commands=["Верхняя_одежда/", 'all_preorders_director'])
    dp.register_message_handler(all_preorders_underwear, commands=["Нижнее_белье/", 'all_preorders_director'])
    dp.register_message_handler(all_preorders_trousers, commands=["Штаны/", 'all_preorders_director'])
    dp.register_callback_query_handler(complete_delete_preorder,
                                       lambda call: call.data and call.data.startswith("delete_preorder"))
