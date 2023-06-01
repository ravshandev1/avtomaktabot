from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def menu_instructor(lang: str):
    if lang == 'uz':
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="👨‍✈️️Профил"),
                    KeyboardButton(text="👨‍✈️Профилни ўзгартириш"),
                ],
                [
                    KeyboardButton(text="👨‍✈️Профилни ўчириш"),
                    KeyboardButton(text='Машғулот нархлари'),
                ],
                [
                    # KeyboardButton(text="Балансни тўлдириш"),
                    KeyboardButton(text="👨‍✈️Машғулотлар рўйхати"),
                ],
                # [
                #     KeyboardButton(text="Бот ҳисобингиздан оладиган хизмат ҳақи"),
                # ],
            ],
            resize_keyboard=True
        )
    else:
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="👨‍✈️️Профиль"),
                    KeyboardButton(text="👨‍✈️Изменение профиля"),
                ],
                [
                    KeyboardButton(text="👨‍✈️Удалить профиль"),
                    KeyboardButton(text='Цены на обучение'),
                ],
                [
                    # KeyboardButton(text="Пополнение баланса"),
                    KeyboardButton(text="👨‍✈️Список занятий"),
                ],
                # [
                #     KeyboardButton(text="Плата за обслуживание, которую бот взимает с вашего баланса"),
                # ],
            ],
            resize_keyboard=True
        )
    return markup


def menu_client(lang: str):
    if lang == 'uz':
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Профил"),
                    KeyboardButton(text="Профилни ўзгартириш"),
                ],
                [
                    KeyboardButton(text="Профилни ўчириш"),
                    KeyboardButton(text="Машғулот"),
                ],
                [
                    KeyboardButton(text='Машғулот нархлари')
                ]
            ],
            resize_keyboard=True
        )
    else:
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Профиль"),
                    KeyboardButton(text="Изменение профиля"),
                ],
                [
                    KeyboardButton(text="Удалить профиль"),
                    KeyboardButton(text="Тренировка"),
                ],
                [
                    KeyboardButton(text='Цены на обучение')
                ]
            ],
            resize_keyboard=True
        )
    return markup


def action_session(lang: str):
    if lang == 'uz':
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Машғулотлар рўйхати"),
                    KeyboardButton(text="Машғулот яратиш"),
                ],
                [
                    KeyboardButton(text="Бош меню")
                ]
            ],
            resize_keyboard=True
        )
    else:
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Список занятий"),
                    KeyboardButton(text="Создание тренировок"),
                ],
                [
                    KeyboardButton(text="Главное меню")
                ]
            ],
            resize_keyboard=True
        )
    return markup


def sessions(lang: str):
    if lang == 'uz':
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Бўлиб утган"),
                    KeyboardButton(text="Бўлиши керак"),
                ],
                [
                    KeyboardButton(text="Бош меню"),
                    KeyboardButton(text="⬅️Oртга"),
                ]
            ],
            resize_keyboard=True
        )
    else:
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Прошедший"),
                    KeyboardButton(text="Должен быть"),
                ],
                [
                    KeyboardButton(text="Главное меню"),
                    KeyboardButton(text="⬅️Назад"),
                ]
            ],
            resize_keyboard=True
        )
    return markup


def edit_session(lang: str):
    if lang == 'uz':
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Машғулотни бекор килиш'),
                    KeyboardButton(text='Машғулот манзилини олиш'),
                ],
                [
                    KeyboardButton(text="Бош меню")
                ]
            ],
            resize_keyboard=True
        )
    else:
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Отменить тренировку'),
                    KeyboardButton(text='Получение адреса для обучения'),
                ],
                [
                    KeyboardButton(text="Главное меню")
                ]
            ],
            resize_keyboard=True
        )
    return markup


def profile_delete(lang: str):
    if lang == 'uz':
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Ҳа'),
                    KeyboardButton(text='Йўқ'),
                ]
            ],
            resize_keyboard=True
        )
    else:
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Да'),
                    KeyboardButton(text='Нет'),
                ]
            ],
            resize_keyboard=True
        )
    return markup


def location_btn(lang: str):
    if lang == 'uz':
        markup = ReplyKeyboardMarkup(keyboard=[
            [
                KeyboardButton(text='Манзилингизни юборинг!', request_location=True)
            ]
        ], resize_keyboard=True)
    else:
        markup = ReplyKeyboardMarkup(keyboard=[
            [
                KeyboardButton(text='Пришлите свой локация!', request_location=True)
            ]
        ], resize_keyboard=True)
    return markup
