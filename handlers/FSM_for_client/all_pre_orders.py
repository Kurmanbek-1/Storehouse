from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import POSTGRES_URL, bot, Admins, Director
from db.utils import get_preorder_from_category, get_preorder_photos
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import asyncpg
import buttons


# =======================================================================================================================

class all_preorders_fsm(StatesGroup):
    category = State()
    more_preorders = State()


async def fsm_start(message: types.Message):
    if message.from_user.id in Admins or Director:
        await message.answer("Эта кнопка для клиентов!")
    else:
        await all_preorders_fsm.category.set()
        await message.answer(f"Категория предзаказа?", reply_markup=buttons.CategoryButtons)


"""Вывод категорий"""
async def load_category(message: types.Message, state: FSMContext):
    if message.text.startswith("/"):
        category = message.text.replace("/", "")
        pool = await asyncpg.create_pool(POSTGRES_URL)
        preorders = await get_preorder_from_category(pool, category)

        if preorders:
            if preorders:
                if len(preorders) <= 5:
                    for preorder in preorders:
                        preorder_info = (
                            f"Информация: {preorder['info']}\n"
                            f"Категория: {preorder['category']}\n"
                            f"Артикул: {preorder['preorder_article']}\n"
                            f"Количество: {preorder['quantity']}\n"
                            f"Дата выхода: {preorder['product_release_date']}\n"
                            f"Цена: {preorder['price']}"
                        )

                        photos = await get_preorder_photos(pool, preorder['id'])
                        photo_urls = [photo['photo'] for photo in photos]

                        media_group = [types.InputMediaPhoto(media=image) for image in photo_urls[:-1]]

                        last_image = photo_urls[-1]
                        last_media = types.InputMediaPhoto(media=last_image, caption=preorder_info)

                        media_group.append(last_media)

                        await bot.send_media_group(chat_id=message.chat.id, media=media_group)
                    await state.finish()
                    await message.answer(f"Это все предзаказы из категории: {category}",
                                         reply_markup=buttons.StartClient)
            else:
                chunks = [preorders[i:i + 5] for i in range(0, len(preorders), 5)]
                data = await state.get_data()
                current_chunk = data.get("current_chunk", 0)
                current_preorders = chunks[current_chunk]

                for preorder in current_preorders:
                    product_info = (
                        f"Информация: {preorder['info']}\n"
                        f"Категория: {preorder['category']}\n"
                        f"Артикул: {preorder['preorder_article']}\n"
                        f"Количество: {preorder['quantity']}\n"
                        f"Дата выхода: {preorder['product_release_date']}\n"
                        f"Цена: {preorder['price']}"
                    )

                    photos = await get_preorder_photos(pool, preorder['id'])
                    photo_urls = [photo['photo'] for photo in photos]

                    media_group = [types.InputMediaPhoto(media=image) for image in photo_urls[:-1]]

                    last_image = photo_urls[-1]
                    last_media = types.InputMediaPhoto(media=last_image, caption=product_info)

                    media_group.append(last_media)

                    await bot.send_media_group(chat_id=message.chat.id, media=media_group)

                await state.update_data(current_chunk=current_chunk + 1)

                if current_chunk < len(chunks) - 1:
                    ShowMore = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
                    ShowMore.add(KeyboardButton(f'Ещё из категории: {category}'))
                    ShowMore.add(KeyboardButton('Отмена'))
                    await message.answer("Показать еще?", reply_markup=ShowMore)
                    await all_preorders_fsm.next()
        else:
            await message.answer("В выбранной категории нет предзаказов")
    else:
        category = message.text.split()[-1]
        pool = await asyncpg.create_pool(POSTGRES_URL)
        preorders = await get_preorder_from_category(pool, category)

        if preorders:
            chunks = [preorders[i:i + 5] for i in range(0, len(preorders), 5)]
            data = await state.get_data()
            current_chunk = data.get("current_chunk", 0)
            current_preorders = chunks[current_chunk]

            for preorder in current_preorders:
                product_info = (
                    f"Информация: {preorder['info']}\n"
                    f"Категория: {preorder['category']}\n"
                    f"Артикул: {preorder['preorder_article']}\n"
                    f"Количество: {preorder['quantity']}\n"
                    f"Дата выхода: {preorder['product_release_date']}\n"
                    f"Цена: {preorder['price']}"
                )

                photos = await get_preorder_photos(pool, preorder['id'])
                photo_urls = [photo['photo'] for photo in photos]

                media_group = [types.InputMediaPhoto(media=image) for image in photo_urls[:-1]]

                last_image = photo_urls[-1]
                last_media = types.InputMediaPhoto(media=last_image, caption=product_info)

                media_group.append(last_media)

                await bot.send_media_group(chat_id=message.chat.id, media=media_group)

            await state.update_data(current_chunk=current_chunk + 1)

            if current_chunk < len(chunks) - 1:
                ShowMore = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
                ShowMore.add(KeyboardButton(f'Ещё из категории: {category}'))
                ShowMore.add(KeyboardButton('Отмена'))
                await message.answer("Показать еще?", reply_markup=ShowMore)
                await all_preorders_fsm.more_preorders.set()
            else:
                await state.finish()
                await message.answer(f"Это все предзаказы из категории: {category}",
                                     reply_markup=buttons.StartClient)
        else:
            await message.answer("В выбранной категории нет предзаказов")


async def load_more_preorders(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await load_category(message, state)


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=buttons.StartClient)


# =======================================================================================================================
def register_all_preorders(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals="Отмена", ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands=["Предзаказы!", 'all_pre_orders'])
    dp.register_message_handler(load_category, state=all_preorders_fsm.category)
    for category in ["Обувь", "Нижнее_белье", "Акссесуары", "Верхняя_одежда", "Штаны"]:
        dp.register_message_handler(load_more_preorders,
                                    Text(equals=f'Ещё из категории: {category}', ignore_case=True),
                                    state=all_preorders_fsm.more_preorders)