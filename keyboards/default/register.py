from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import requests
from data.config import BASE_URL

usertype = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Client'),
            KeyboardButton(text='Instructor'),
        ]
    ],
    resize_keyboard=True
)
prava = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Bor'),
            KeyboardButton(text="Yo'q"),
        ],
    ],
    resize_keyboard=True
)
where = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Avtomaktabdan'),
            KeyboardButton(text="Uydan"),
        ],
    ],
    resize_keyboard=True
)
genders = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Erkak'),
            KeyboardButton(text='Ayol'),
        ]
    ],
    resize_keyboard=True
)
payment = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Naqd'),
            KeyboardButton(text='Karta'),
        ]
    ],
    resize_keyboard=True
)
str_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Boshlash')
        ]
    ],
    resize_keyboard=True
)
stp_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Tugatish')
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
