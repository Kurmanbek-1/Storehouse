from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, Admins
import buttons


# =======================================================================================================================

class FSM_pre_order(StatesGroup):
    articule = State()
    quantity = State()
    number = State()
    fullname = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.from_user.id in Admins:
        await message.answer('Вы сотдруник или админ, вы не можете оформить предзаказ!')
    else:
        await FSM_pre_order.articule.set()
        await message.answer("Артикул товара?!", reply_markup=buttons.cancel_markup_for_client)


async def data_arcticle(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['articule'] = message.text
    await FSM_pre_order.next()
    await message.answer('Количество товаров?')


async def data_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quantity'] = message.text
    await FSM_pre_order.next()
    await message.answer("Ваш номер телефона или то через что мы сможем с вами связаться!\n\n"
                         "(Instagram, Telegram, WhatsAppи или телефон номер!)")


async def data_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = message.text
    await FSM_pre_order.next()
    await message.answer("Ваше ФИО?\n"
                         "(Фамилия Имя Отчество)")


async def data_fullname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fullname'] = message.text

    await message.answer(f"Артикул: {data['articule']}\n"
                         f"Количество товара: {data['quantity']}\n"
                         f"Телефон номер или соц.сеть: {data['number']}\n"
                         f"ФИО: {data['fullname']}", reply_markup=buttons.submit_markup)
    await FSM_pre_order.next()
    await message.answer('Верно?!')


async def load_submit(message: types.Message, state: FSMContext):
    if message.text == "да":
        await message.answer('Отправлено менеджерам!', reply_markup=buttons.StartClient)

        async with state.proxy() as data:
            values = (
                data['articule'],
                data['quantity'],
                data['number'],
                data['fullname']
            )
        photo = open('media/for_pre_order.png', 'rb')
        for admin in Admins:
            await bot.send_photo(photo=photo, chat_id=admin, caption=f"Артикул: {data['articule']}\n"
                                                                     f"Количество товара: {data['quantity']}\n"
                                                                     f"Телефон номер или соц.сеть: {data['number']}\n"
                                                                     f"ФИО: {data['fullname']}")

        await state.finish
        # Запись в базу данных

    elif message.text.lower() == "нет":
        await message.answer('Отменено!', reply_markup=buttons.StartClient)
        await state.finish()

    else:
        await message.answer("Пожалуйста, выберите Да или Нет.")


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=buttons.StartClient)


# =======================================================================================================================
def register_pre_order(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals="Отмена", ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands=["Предзаказать", "pre_order"])
    dp.register_message_handler(data_arcticle, state=FSM_pre_order.articule)
    dp.register_message_handler(data_quantity, state=FSM_pre_order.quantity)
    dp.register_message_handler(data_number, state=FSM_pre_order.number)
    dp.register_message_handler(data_fullname, state=FSM_pre_order.fullname)
    dp.register_message_handler(load_submit, state=FSM_pre_order.submit)
