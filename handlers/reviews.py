from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from config import POSTGRES_URL, bot, Director, Admins
from db.ORM import get_all_reviews

import asyncpg
import buttons


async def reviews_for_directors(message: types.Message):
    if message.from_user.id in Director:
        pool = await asyncpg.create_pool(POSTGRES_URL)
        reviews = await get_all_reviews(pool)

        if reviews:
            for review in reviews:
                review_info = (
                    f"Артикул товара: {review['article_number']}\n"
                    f"Название товара: {review['info_product']}\n"
                    f"Отзыв: {review['review']}/5"
                )

                if review['photo_review']:
                    await bot.send_photo(chat_id=message.chat.id,
                                         photo=review['photo_review'],
                                         caption=review_info,
                                         reply_markup=buttons.StartDirector)
                else:
                    await message.answer(review_info, reply_markup=buttons.StartDirector)
    elif message.from_user.id in Admins:
        await message.answer('Вы не директор!', reply_markup=buttons.StartAdmin)
    else:
        await message.answer('Вы не директор!', reply_markup=buttons.StartClient)


def register_all_reviews_for_directors(dp: Dispatcher):
    dp.register_message_handler(reviews_for_directors, commands=["Отзывы", 'reviews'])