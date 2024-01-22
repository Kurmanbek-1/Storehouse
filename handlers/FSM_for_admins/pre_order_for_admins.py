from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, Admins
import buttons


# =======================================================================================================================

class FSM_pre_order_for_admins(StatesGroup):
    info = State()
    articule = State()
    quantity = State()
    category = State()
    price = State()
    date = State()
    photos = State()
    submit = State()


media_group = types.MediaGroup()


async def fsm_start(message: types.Message):
    if message.from_user.id in Admins:
        await FSM_pre_order_for_admins.info.set()
        await message.answer("Информация о товаре?!", reply_markup=buttons.cancel_markup_for_admins)
    else:
        await message.answer('Вы не админ!')


async def load_info(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['info'] = message.text
    await FSM_pre_order_for_admins.next()
    await message.answer('Артикул товара?')


async def data_arcticule(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['articule'] = message.text
    await FSM_pre_order_for_admins.next()
    await message.answer('Количество товаров?')


async def load_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quantity'] = message.text
    await FSM_pre_order_for_admins.next()
    await message.answer('Категория товаров?', reply_markup=buttons.CategoryButtons)


async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text.replace("/", "")

    await FSM_pre_order_for_admins.next()
    await message.answer("Цена товара?")


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await FSM_pre_order_for_admins.next()
    await message.answer("Дата выхода?")


async def load_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
    await FSM_pre_order_for_admins.next()
    await message.answer("Отправьте фотографии")


async def load_photos(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if "photos" in data:
            data["photos"].append(message.photo[-1].file_id)
        else:
            data["photos"] = [message.photo[-1].file_id]

    await message.answer(f"Добавлено!", reply_markup=buttons.finish_load_photos)


async def finish_load_photos(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        last_photo = None

        for i in data['photos']:
            if i in media_group:
                pass
            last_photo = types.InputMediaPhoto(i)
            media_group.attach_photo(last_photo)

        await bot.send_media_group(chat_id=message.from_user.id, media=media_group)
        await message.answer(text=f"Информация: {data['info']}\n"
                                  f"Артикул: {data['articule']}\n"
                                  f"Количество товара: {data['quantity']}\n"
                                  f"Категория: {data['category']}"
                                  f"Цена: {data['price']}", reply_markup=buttons.submit_markup)

        await message.answer("Всё правильно?", reply_markup=buttons.submit_markup)
        await FSM_pre_order_for_admins.next()


async def load_submit(message: types.Message, state: FSMContext):
    if message.text == "да":
        await message.answer('Записано! ✅', reply_markup=buttons.StartAdmin)
        # Запись в базу данных
        await state.finish()

    elif message.text.lower() == "нет":
        await message.answer('Отменено!', reply_markup=buttons.StartClient)
        await state.finish()

    else:
        await message.answer("Пожалуйста, выберите Да или Нет.")


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=buttons.StartAdmin)


# =======================================================================================================================
def register_pre_order_for_admins(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals="Отмена!", ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands=["Заполнить_предзаказ"])

    dp.register_message_handler(load_info, state=FSM_pre_order_for_admins.info)
    dp.register_message_handler(data_arcticule, state=FSM_pre_order_for_admins.articule)
    dp.register_message_handler(load_quantity, state=FSM_pre_order_for_admins.quantity)
    dp.register_message_handler(load_category, state=FSM_pre_order_for_admins.category)
    dp.register_message_handler(load_price, state=FSM_pre_order_for_admins.price)
    dp.register_message_handler(load_date, state=FSM_pre_order_for_admins.date)

    dp.register_message_handler(load_photos, state=FSM_pre_order_for_admins.photos, content_types=['photo'])
    dp.register_message_handler(finish_load_photos, commands=['Сохранить_фотки!'],
                                state=FSM_pre_order_for_admins.photos)

    dp.register_message_handler(load_submit, state=FSM_pre_order_for_admins.submit)
