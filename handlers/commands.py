from aiogram import Dispatcher, types
from config import Admins
from keyboards import buttons


async def start(message: types.Message):
    if message.from_user.id in Admins:
        await message.answer('',
                             reply_markup=None)

    else:
        await message.answer('', reply_markup=buttons.StartClient)


async def support(message: types.Message):
    await message.answer('Наша тех.поддержка: ', reply_markup=buttons.StartClient)


def register_commands(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(support, commands=['support'])
