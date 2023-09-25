from aiogram import types
from loader import dp
import requests
from data.config import BASE_URL
from keyboards.default.is_authenticated import menu_instructor, menu_client
from keyboards.default.register import usertype
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline.edit_profile import change_lang

lang = ''


@dp.message_handler(CommandStart())
async def stt(mes: types.Message):
    res = requests.get(url=f"{BASE_URL}/session/user/?id={mes.from_user.id}")
    r = res.json()
    # if r['message'] == "Client":
    #     if lang == 'ru':
    #         await mes.answer("Выберите нужный раздел 👇", reply_markup=menu_client(lang))
    #     else:
    #         await mes.answer("Керакли булимни танланг 👇", reply_markup=menu_client(lang))
    if r['message'] == "Instructor":
        if lang == 'ru':
            await mes.answer("Выберите нужный раздел 👇", reply_markup=menu_instructor(lang))
        else:
            await mes.answer("Керакли булимни танланг 👇", reply_markup=menu_instructor(lang))
    else:
        await mes.answer(
            f"Ассалому алайкум, {mes.from_user.full_name}!\nАвтоинструктор ботга хуш келибсиз\nВыберите язык / Тилни танланг",
            reply_markup=change_lang)


@dp.callback_query_handler(text=['uz', 'ru'])
async def start(call: types.CallbackQuery):
    res = requests.get(url=f"{BASE_URL}/session/user/?id={call.from_user.id}")
    r = res.json()
    await call.message.delete()
    await call.answer(cache_time=3)
    global lang
    # if r['message'] == "Client":
    #     if call.data == 'uz':
    #         lang = 'uz'
    #         await call.message.answer("Керакли булимни танланг 👇", reply_markup=menu_client(lang))
    #     elif call.data == 'ru':
    #         lang = 'ru'
    #         await call.message.answer("Выберите нужный раздел 👇", reply_markup=menu_client(lang))
    if r['message'] == "Instructor":
        if call.data == 'uz':
            lang = 'uz'
            await call.message.answer("Керакли булимни танланг 👇", reply_markup=menu_instructor(lang))
        elif call.data == 'ru':
            lang = 'ru'
            await call.message.answer("Выберите нужный раздел 👇", reply_markup=menu_instructor(lang))
    else:
        if call.data == 'uz':
            lang = 'uz'
            await call.message.answer(
                f"Ассалому алайкум, {call.from_user.full_name}!\nАвтоинструктор ботга хуш келибсиз. Ботимиздан фойдаланиш учун ўзингизга керакли бўлимни танланг.",
                reply_markup=usertype(lang))
        elif call.data == 'ru':
            lang = 'ru'
            await call.message.answer(
                f"Здравствуйте, {call.from_user.full_name}!\nДобро пожаловать в Автоинструктор бот.Выберите для себя нужный раздел",
                reply_markup=usertype(lang))
