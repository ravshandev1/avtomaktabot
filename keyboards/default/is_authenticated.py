from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_instructor = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👨‍✈️Profile"),
            KeyboardButton(text="👨‍✈️Profileni o'zgartirish"),
        ],
        [
            KeyboardButton(text="Balansni to'ldirish"),
            KeyboardButton(text="Darslar ro'yxati"),
        ],
        [
            KeyboardButton(text="Profileni o'chirish")
        ]
    ],
    resize_keyboard=True
)

menu_client = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Profile"),
            KeyboardButton(text="Profileni o\'zgartirish"),
        ],
        [
            KeyboardButton(text="Profileni o'chirish"),
            KeyboardButton(text="Session"),
        ]
    ],
    resize_keyboard=True
)
action_session = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Sessionlar ro\'yxati"),
            KeyboardButton(text="Session yaratish"),
        ],
        [
            KeyboardButton(text="Bosh menu")
        ]
    ],
    resize_keyboard=True
)

sessions = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Bo'lib o'tgan"),
            KeyboardButton(text="Bo'lishi kerak"),
        ],
        [
            KeyboardButton(text="Bosh menu")
        ]
    ],
    resize_keyboard=True
)

edit_session = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Sessionni o\'chirish'),
        ],
        [
            KeyboardButton(text="Bosh menu")
        ]
    ],
    resize_keyboard=True
)
