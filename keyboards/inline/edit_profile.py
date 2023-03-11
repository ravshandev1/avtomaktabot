from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

client = InlineKeyboardMarkup(
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

instructor = InlineKeyboardMarkup(
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
            InlineKeyboardButton(text='Мошинани номерини', callback_data='number'),
            InlineKeyboardButton(text='Манзилини', callback_data='locate'),
        ]
    ]
)
