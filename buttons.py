from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# ======================================================================================================================
StartClient = ReplyKeyboardMarkup(resize_keyboard=True,
                                  one_time_keyboard=True,
                                  row_width=2
                                  ).add(KeyboardButton('/Товары!'),
                                        KeyboardButton('/Предзаказы!'),
                                        KeyboardButton('/Заказать!'),
                                        KeyboardButton('/Предзаказать'),
                                        KeyboardButton('/ТехПоддержка'),
                                        KeyboardButton('/Написать_отзыв'),
                                        KeyboardButton('/Поиск'))

StartDirector = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True,
                                    row_width=2
                                    ).add(KeyboardButton('/Товары*'),
                                          KeyboardButton('/Предзаказы*'),
                                          KeyboardButton('/Отзывы'),
                                          KeyboardButton('/Поиск'))

StartAdmin = ReplyKeyboardMarkup(resize_keyboard=True,
                                 one_time_keyboard=True,
                                 row_width=2
                                 ).add(KeyboardButton('/Заказы'),
                                       KeyboardButton('/Предзаказы'),
                                       KeyboardButton('/Заполнить_товар!'),
                                       KeyboardButton('/Заполнить_предзаказ'),
                                       KeyboardButton('/Поиск'))

CancelSearch = ReplyKeyboardMarkup(resize_keyboard=True,
                                 one_time_keyboard=True,
                                 row_width=2
                                 ).add(KeyboardButton('/Выход из поиска🚫'))

ShowMore = ReplyKeyboardMarkup(resize_keyboard=True,
                                 one_time_keyboard=True,
                                 row_width=2
                                 ).add(KeyboardButton('Далее'))

cancel_button_for_client = KeyboardButton('Отмена')
cancel_markup_for_client = ReplyKeyboardMarkup(resize_keyboard=True,
                                               one_time_keyboard=True,
                                               ).add(cancel_button_for_client)

cancel_button_for_admins = KeyboardButton('Отмена!')
cancel_markup_for_admins = ReplyKeyboardMarkup(resize_keyboard=True,
                                               one_time_keyboard=True,
                                               ).add(cancel_button_for_admins)

cancel_button_for_director = KeyboardButton('/Отмена🚫')
cancel_markup_for_director = ReplyKeyboardMarkup(resize_keyboard=True,
                                               one_time_keyboard=True,
                                               ).add(cancel_button_for_director)

submit_markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True
                                    ).add(KeyboardButton('да'),
                                          KeyboardButton('нет'))

finish_load_photos = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add \
    (KeyboardButton('/Сохранить_фотки!'))

CategoryButtons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
m1 = KeyboardButton('/Обувь')
m2 = KeyboardButton('/Нижнее_белье')
m3 = KeyboardButton('/Акссесуары')
m4 = KeyboardButton('/Верхняя_одежда')
m5 = KeyboardButton('/Штаны')
CategoryButtons.add(m1, m2, m3, m4, m5, cancel_button_for_client)


CategoryButtonsAdmins = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
m1 = KeyboardButton('/Обувь')
m2 = KeyboardButton('/Нижнее_белье')
m3 = KeyboardButton('/Акссесуары')
m4 = KeyboardButton('/Верхняя_одежда')
m5 = KeyboardButton('/Штаны')
CategoryButtonsAdmins.add(m1, m2, m3, m4, m5, cancel_button_for_admins)


CategoryButtonsDirector = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
m1 = KeyboardButton('/Обувь')
m2 = KeyboardButton('/Нижнее_белье')
m3 = KeyboardButton('/Акссесуары')
m4 = KeyboardButton('/Верхняя_одежда')
m5 = KeyboardButton('/Штаны')
CategoryButtonsDirector.add(m1, m2, m3, m4, m5, cancel_button_for_director)