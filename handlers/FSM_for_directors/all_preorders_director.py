from aiogram import types, Dispatcher
from config import POSTGRES_URL, bot, Director
from db.utils import get_preorder_from_category, get_preorder_photos
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from db.ORM import delete_preorder
import asyncpg
import buttons
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

# =======================================================================================================================
class PreorderStates(StatesGroup):
    category = State()
    more_preorders = State()

async def fsm_start(message: types.Message):
    if message.from_user.id in Director:
        await PreorderStates.category.set()
        await message.answer("Выберите категорию предзаказа:", reply_markup=buttons.CategoryButtonsDirector)
    else:
        await message.answer('Вы не директор!')

async def load_preorder_category(message: types.Message, state: FSMContext):
    if message.from_user.id in Director:
        if message.text.startswith("/"):
            category = message.text.replace("/", "")
            pool = await asyncpg.create_pool(POSTGRES_URL)
            preorders = await get_preorder_from_category(pool, category)

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

                    await state.finish()
                    await message.answer(f"Это все предзаказы из категории: {category}",
                                         reply_markup=buttons.StartDirector)
                    await message.answer("Чтобы удалить предзаказ нажмите на кнопку 'Удалить' под сообщением")
                else:
                    chunks = [preorders[i:i + 5] for i in range(0, len(preorders), 5)]
                    data = await state.get_data()
                    current_chunk = data.get("current_chunk", 0)
                    current_preorders = chunks[current_chunk]

                    for preorder in current_preorders:
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

                    await state.update_data(current_chunk=current_chunk + 1)

                    if current_chunk < len(chunks) - 1:
                        ShowMore = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
                        ShowMore.add(KeyboardButton(f'Ещё из категории: {category}'))
                        ShowMore.add(KeyboardButton('/Отмена🚫'))
                        await message.answer("Показать еще?", reply_markup=ShowMore)
                        await message.answer("Чтобы удалить предзаказ, нажмите на кнопку (/Отмена🚫), "
                                             "либо выведите все предзаказы до конца!")
                        await PreorderStates.next()
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

                await state.update_data(current_chunk=current_chunk + 1)

                if current_chunk < len(chunks) - 1:
                    ShowMore = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
                    ShowMore.add(KeyboardButton(f'Ещё из категории: {category}'))
                    ShowMore.add(KeyboardButton('/Отмена🚫'))
                    await message.answer("Показать еще?", reply_markup=ShowMore)
                    await message.answer("Чтобы удалить предзаказ, нажмите на кнопку (/Отмена🚫), "
                                         "либо выведите все предзаказы до конца!")
                    await PreorderStates.more_preorders.set()
                else:
                    await state.finish()
                    await message.answer(f"Это все предзаказы из категории: {category}",
                                         reply_markup=buttons.StartDirector)
                    await message.answer("Чтобы удалить предзаказ нажмите на кнопку 'Удалить' под сообщением")
            else:
                await message.answer("В выбранной категории нет предзаказов")

    else:
        await message.answer('Вы не директор!')

async def complete_delete_preorder(call: types.CallbackQuery):
    preorder_id = call.data.replace("delete_preorder", "").strip()
    await delete_preorder(preorder_id)
    await call.message.reply(text="Удалено из базы данных")

async def load_more(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await load_preorder_category(message, state)

async def cancel_reg(message: types.Message, state: FSMContext):
    if message.from_user.id in Director:
        current_state = await state.get_state()
        if current_state is not None:
            await state.finish()
            await message.answer('Отменено!', reply_markup=buttons.StartDirector)
            await message.answer("Чтобы удалить предзаказ нажмите на кнопку 'Удалить' под сообщением")
    else:
        await message.answer('Вы не директор!')

# =======================================================================================================================
def register_all_preorders_director(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals="/Отмена🚫", ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands=["Предзаказы*", 'all_preorders_director'])
    dp.register_message_handler(load_preorder_category, state=PreorderStates.category)
    for category in ["Обувь", "Нижнее_белье", "Акссесуары", "Верхняя_одежда", "Штаны"]:
        dp.register_message_handler(load_more, Text(equals=f"Ещё из категории: {category}", ignore_case=True),
                                    state=PreorderStates.more_preorders)
    dp.register_callback_query_handler(complete_delete_preorder,
                                       lambda call: call.data and call.data.startswith("delete_preorder"))
