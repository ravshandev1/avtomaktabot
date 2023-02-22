from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

client = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Ismni', callback_data="client:name"),
            InlineKeyboardButton(text='Familiyani', callback_data='client:surname'),
        ],
        [
            InlineKeyboardButton(text='Telefon raqamni', callback_data='client:phone'),
            InlineKeyboardButton(text='Pravani', callback_data='pra'),
        ]
    ]
)

instructor = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Ismni', callback_data='instructor:name'),
            InlineKeyboardButton(text='Familiya', callback_data='instructor:surname'),
            InlineKeyboardButton(text='Telefon raqamni', callback_data='instructor:phone'),
        ],
        [
            InlineKeyboardButton(text='Yashash tumanni', callback_data='region'),
            InlineKeyboardButton(text='Toifamni', callback_data='cat'),
            InlineKeyboardButton(text='Moshina', callback_data='car'),
        ],
        [
            InlineKeyboardButton(text='Moshinani nomerini', callback_data='number')
        ]
    ]
)
