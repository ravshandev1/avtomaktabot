from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def client(lang: str):
    if lang == 'uz':
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='Исмни', callback_data="client:name"),
                    InlineKeyboardButton(text='Фамилияни', callback_data='client:surname'),
                ],
                [
                    InlineKeyboardButton(text='Телефон рақамни', callback_data='client:phone'),
                    InlineKeyboardButton(text='Правани', callback_data='pra'),
                ]
            ]
        )
    else:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='Имя', callback_data="client:name"),
                    InlineKeyboardButton(text='Фамилия', callback_data='client:surname'),
                ],
                [
                    InlineKeyboardButton(text='Номер телефона', callback_data='client:phone'),
                    InlineKeyboardButton(text='Водительские права', callback_data='pra'),
                ]
            ]
        )
    return markup


def instructor(lang: str):
    if lang == 'uz':
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='Исмни', callback_data='instructor:name'),
                    InlineKeyboardButton(text='Фамилияни', callback_data='instructor:surname'),
                    InlineKeyboardButton(text='Телефон рақамни', callback_data='instructor:phone'),
                ],
                [
                    InlineKeyboardButton(text='Яшаш туманни', callback_data='region'),
                    InlineKeyboardButton(text='Тоифамни', callback_data='cat'),
                    InlineKeyboardButton(text='Мошинани', callback_data='car'),
                ],
                [
                    InlineKeyboardButton(text='Давлат рақамини', callback_data='number'),
                    InlineKeyboardButton(text='Манзилини', callback_data='locate'),
                    InlineKeyboardButton(text='Тўлов турини', callback_data='cart'),
                ]
            ]
        )
    else:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='Имя', callback_data='instructor:name'),
                    InlineKeyboardButton(text='Фамилия', callback_data='instructor:surname'),
                    InlineKeyboardButton(text='Номер телефона', callback_data='instructor:phone'),
                ],
                [
                    InlineKeyboardButton(text='Район', callback_data='region'),
                    InlineKeyboardButton(text='Моя категория', callback_data='cat'),
                    InlineKeyboardButton(text='Автомобиль', callback_data='car'),
                ],
                [
                    InlineKeyboardButton(text='Гос.номер', callback_data='number'),
                    InlineKeyboardButton(text='Адрес', callback_data='locate'),
                    InlineKeyboardButton(text='Способ оплаты', callback_data='cart'),
                ]
            ]
        )
    return markup


change_lang = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 Ўзбек тили", callback_data="uz"),
            InlineKeyboardButton(text="🇷🇺 Русский язык", callback_data="ru"),
        ]
    ]
)
