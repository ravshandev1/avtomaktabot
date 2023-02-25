from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import requests
from data.config import BASE_URL

usertype = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ўрганувчи'),
            KeyboardButton(text='Инструктор'),
        ]
    ],
    resize_keyboard=True
)
prava = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Бор'),
            KeyboardButton(text="Юқ"),
        ],
    ],
    resize_keyboard=True
)
where = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Автомактабдан'),
            KeyboardButton(text="Уйдан"),
        ],
    ],
    resize_keyboard=True
)
genders = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Еркак'),
            KeyboardButton(text='Аёл'),
        ]
    ],
    resize_keyboard=True
)
payment = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Накд'),
            KeyboardButton(text='Карта'),
        ]
    ],
    resize_keyboard=True
)
str_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Бошлаш')
        ]
    ],
    resize_keyboard=True
)
stp_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Тугатиш')
        ]
    ],
    resize_keyboard=True
)


def regions():
    r = requests.get(url=f"{BASE_URL}/instructor/regions/")
    rg = r.json()
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for i in rg:
        keyboard.insert(
            KeyboardButton(text=f"{i['nomi']}")
        )
    return keyboard


def categories():
    res = requests.get(url=f"{BASE_URL}/session/categories/")
    cats = res.json()
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for i in cats:
        keyboard.insert(
            KeyboardButton(text=f"{i['toifa']}")
        )
    return keyboard
