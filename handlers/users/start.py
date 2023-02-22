from aiogram import types
from loader import dp
import requests
from data.config import BASE_URL
from keyboards.default.is_authenticated import menu_instructor, menu_client
from keyboards.default.register import usertype


@dp.message_handler(state=None)
async def start(message: types.Message):
    res = requests.get(url=f"{BASE_URL}/session/user/?id={message.from_user.id}")
    r = res.json()
    if r['message'] == "Client":
        await message.answer("Kerakli bo'limni tanlang 👇", reply_markup=menu_client)
    elif r['message'] == "Instructor":
        await message.answer("Kerakli bo'limni tanlang 👇", reply_markup=menu_instructor)
    else:
        await message.answer(
            f"Salom, {message.from_user.full_name}!\nBotimizga xush kelibsiz. Botimizdan kim sifatida ro'yxatdan o'tmoqchisiz?",
            reply_markup=usertype)
