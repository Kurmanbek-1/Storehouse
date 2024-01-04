from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# ======================================================================================================================
StartClient = ReplyKeyboardMarkup(resize_keyboard=True,
                                  one_time_keyboard=True
                                  ).add(KeyboardButton('/Предзаказать'),
                                        KeyboardButton('/'))

StartAdmin = ReplyKeyboardMarkup(resize_keyboard=True,
                                 one_time_keyboard=True
                                 ).add(KeyboardButton('/Предзаказы'))


cancel_button = KeyboardButton('Отмена')
cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True,
                                    ).add(cancel_button)

submit_markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True
                                    ).add(KeyboardButton('да'),
                                          KeyboardButton('нет'))

yesno = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    row_width=2).add(KeyboardButton('Да'),
                     KeyboardButton('Нет'),
                     cancel_button)