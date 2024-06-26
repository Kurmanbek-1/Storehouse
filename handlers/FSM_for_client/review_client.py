from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import Admins
import buttons
from datetime import datetime
from db.ORM import save_reviews_info

# =======================================================================================================================


class review_fsm(StatesGroup):
    articule = State()
    name = State()
    review = State()
    submit_photo = State()
    photo = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.from_user.id in Admins:
        await message.answer('Вы сотдруник или админ, вы не можете оcтавить отзыв!')
    else:
        await review_fsm.articule.set()
        await message.answer("Артикуль товара?", reply_markup=buttons.cancel_button_for_client)


async def load_articule(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["article_number"] = message.text
    await review_fsm.next()
    await message.answer("Название товара!?")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["info_product"] = message.text
    await review_fsm.next()
    await message.answer("Отзыв о товаре!?\n" "?/5")


async def load_review(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["review"] = message.text
    await review_fsm.next()
    await message.answer("Вы хотите отправить фото товара?", reply_markup=buttons.submit_markup)


async def submit_photo(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await review_fsm.next()
        await message.answer("Отправьте фотку товара")
    elif message.text.lower() == 'нет':
        async with state.proxy() as data:
            data["date"] = datetime.now()
            data["photo_review"] = None
            await message.answer(f"Артикуль товара: {data['article_number']}\n"
                                 f"Название товара: {data['info_product']}\n"
                                 f"Отзыв о товаре: {data['review']}\n")
            await review_fsm.submit.set()
            await message.answer("Все верно?", reply_markup=buttons.submit_markup)
    else:
        await message.answer("Пожалуйста, выберите Да или Нет.", reply_markup=buttons.submit_markup)


# ...

async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["photo_review"] = message.photo[-1].file_id
        data["date"] = datetime.now()
        await message.answer_photo(
            data["photo_review"],
            caption=f"Данные товара: \n"
                    f"Артикуль товара: {data['article_number']}\n"
                    f"Название товара: {data['info_product']}\n"
                    f"Отзыв о товаре: {data['review']}\n")
        await review_fsm.next()
        await message.answer("Все верно?", reply_markup=buttons.submit_markup)


async def load_submit(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        async with state.proxy() as data:
            await save_reviews_info(state)
            await message.answer('Готово!', reply_markup=buttons.StartClient)
            await state.finish()
    elif message.text.lower() == 'нет':
        await message.answer('Хорошо, отменено', reply_markup=buttons.StartClient)
        await state.finish()
    else:
        await message.answer("Пожалуйста, выберите Да или Нет.")



async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=buttons.StartClient)


# =======================================================================================================================


def register_review(dp: Dispatcher):
    dp.register_message_handler(
        cancel_reg, Text(equals="/cancel", ignore_case=True), state="*"
    )
    dp.register_message_handler(fsm_start, commands=["Написать_отзыв", "review"])

    dp.register_message_handler(load_articule, state=review_fsm.articule)
    dp.register_message_handler(load_name, state=review_fsm.name)
    dp.register_message_handler(load_review, state=review_fsm.review)

    dp.register_message_handler(submit_photo, state=review_fsm.submit_photo)
    dp.register_message_handler(load_photo, state=review_fsm.photo, content_types=["photo"])

    dp.register_message_handler(load_submit, state=review_fsm.submit)
