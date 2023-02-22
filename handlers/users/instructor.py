from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery
import requests
from data.config import BASE_URL
from states.instructor import InstructorForm, EditInstructor
from aiogram.dispatcher import FSMContext
from loader import dp
from keyboards.default.register import genders, regions, categories
from keyboards.default.is_authenticated import menu_instructor
from keyboards.inline.edit_profile import instructor
from keyboards.inline.sessions import sessions
import re


@dp.message_handler(text='Instructor')
async def register(mes: Message):
    await InstructorForm.ism.set()
    await mes.answer("Ismingiz:", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=InstructorForm.ism)
async def ism(mes: Message, state: FSMContext):
    await state.update_data(
        {"ism": mes.text}
    )
    await mes.answer("Familiyangiz:")
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.familiya)
async def familiya(mes: Message, state: FSMContext):
    await state.update_data(
        {'familiya': mes.text}
    )
    await mes.answer(
        'Telefon raqamingizni kodi bilan 7 ta raqmini qushib yozing\nMasalan: <b>901234567</b> kurishnishda yozing')
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.telefon, regexp=re.compile(r"^[378]{2}|9[01345789]\d{7}$"))
async def telefon(mes: Message, state: FSMContext):
    await state.update_data(
        {'telefon': f"998{mes.text}"}
    )
    await mes.answer("Jinsingiz: ", reply_markup=genders)
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.jins)
async def gender(mes: Message, state: FSMContext):
    await state.update_data(
        {'jins': mes.text}
    )
    await mes.answer("Yashash tumaningiz: ", reply_markup=regions())
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.tuman)
async def region(mes: Message, state: FSMContext):
    await state.update_data(
        {'tuman': mes.text}
    )
    await mes.answer("Qaysi toifa instruktirisiz: ", reply_markup=categories())
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.toifa)
async def category(mes: Message, state: FSMContext):
    await state.update_data(
        {'toifa': mes.text}
    )
    cat = await state.get_data()
    res = requests.get(url=f"{BASE_URL}/instructor/cars/?cat={cat['toifa']}")
    rg = res.json()
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    for i in rg:
        markup.insert(KeyboardButton(text=f"{i['nomi']}"))
    await mes.answer("Mashinani tanlang: ", reply_markup=markup)
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.moshina)
async def car(mes: Message, state: FSMContext):
    await state.update_data(
        {'moshina': mes.text}
    )
    await mes.answer(
        "Mashinangiz nomerini yozing\nMasalan: <b>01 A 111 AA</b> yoki <b>01 111 AAA</b> ko'rinishida bulsin",
        reply_markup=ReplyKeyboardRemove())
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.nomeri, regexp=re.compile(
    r"^[0-9][150][ -]([A-Z][ -][0-9]{3}[ -][A-Z]{2})|([0-9]{3}[ -][A-Z]{3})$"))
async def create_instructor(mes: Message, state: FSMContext):
    await state.update_data(
        {'nomeri': mes.text, 'telegram_id': mes.from_user.id}
    )
    data = await state.get_data()
    res = requests.post(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    r = res.json()
    await mes.answer(f"{mes.from_user.first_name} {r['message']}", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(text="👨‍✈️Profile")
async def get_profile(mes: Message):
    rp = requests.get(url=f"{BASE_URL}/instructor/{mes.from_user.id}/")
    res = rp.json()
    text = f"Ismingiz: <b>{res['ism']}</b>\n"
    text += f"Familiyangiz: <b>{res['familiya']}</b>\n"
    text += f"Telefon raqamangiz: <b>{res['telefon']}</b>\n"
    text += f"Moshinagiz: <b>{res['moshina']}</b>\n"
    text += f"Yashash tumaningiz: <b>{res['tuman']}</b>\n"
    text += f"Toifangiz: <b>{res['toifa']}</b>\n"
    text += f"Balansizgiz: <b>{res['balans']} so'm</b>\n"
    text += f"Moshinayiz nomeri: <b>{res['nomeri']}</b>\n"
    await mes.answer(text, reply_markup=menu_instructor)


@dp.message_handler(text='👨‍✈️Profileni o\'zgartirish')
async def edit_profile(mes: Message):
    await mes.answer("Nimani o'zgartirmoqchisiz?", reply_markup=instructor)


@dp.callback_query_handler(
    text=['instructor:name', 'instructor:surname', 'instructor:phone', 'car', 'number', 'region', 'cat'])
async def set_state(call: CallbackQuery):
    if call.data == "instructor:name":
        await call.message.answer("Ismingizni yozing:")
        await EditInstructor.ism.set()
    elif call.data == "instructor:surname":
        await call.message.answer("Familiyangizni yozing:")
        await EditInstructor.familiya.set()
    elif call.data == "instructor:phone":
        await call.message.answer(
            "Telefon raqamingizni kodi bilan 7 ta raqmini qushib yozing\nMasalan: <b>901234567</b> kurishnishda yozing")
        await EditInstructor.telefon.set()
    elif call.data == "car":
        res = requests.get(url=f"{BASE_URL}/instructor/cars/")
        rg = res.json()
        markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
        for i in rg:
            markup.insert(KeyboardButton(text=f"{i['nomi']}"))
        await call.message.answer("Moshina nomini tanlang:", reply_markup=markup)
        await EditInstructor.moshina.set()
    elif call.data == "region":
        await call.message.answer("Yashash manzilingizni tanlang", reply_markup=regions())
        await EditInstructor.tuman.set()
    elif call.data == 'cat':
        await call.message.answer("Toifani tanlang:", reply_markup=categories())
        await EditInstructor.toifa.set()
    elif call.data == "number":
        await call.message.answer(
            "Mashinangiz nomerini yozing\nMasalan: <b>01 A 111 AA</b> yoki <b>01 111 AAA</b> kurinishida bulsin")
        await EditInstructor.nomeri.set()
    await call.answer(cache_time=3)


@dp.message_handler(content_types=['text'], state=EditInstructor.ism)
async def set_name(mes: Message, state: FSMContext):
    data = {'ism': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    await mes.answer(f"Ismingiz <b>{res['ism']}</b> ga o'zgartirildi!", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(content_types=['text'], state=EditInstructor.familiya)
async def set_surname(mes: Message, state: FSMContext):
    data = {'familiya': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    await mes.answer(f"Familiyangiz <b>{res['familiya']}</b> ga o'zgartirildi!", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(content_types=['text'], state=EditInstructor.telefon)
async def set_phone(mes: Message, state: FSMContext):
    data = {'telefon': f"998{mes.text}"}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    await mes.answer(f"Telefongiz <b>{res['telefon']}</b> ga o'zgartirildi!", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(content_types=['text'], state=EditInstructor.tuman)
async def set_region(mes: Message, state: FSMContext):
    data = {'tuman': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    await mes.answer(f"Yashash tumaningiz <b>{res['tuman']}</b> ga o'zgartirildi!", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(content_types=['text'], state=EditInstructor.toifa)
async def set_cat(mes: Message, state: FSMContext):
    data = {'toifa': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    await mes.answer(f"Toifaningiz <b>{res['toifa']}</b> ga o'zgartirildi!", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(content_types=['text'], state=EditInstructor.nomeri, regexp=re.compile(
    r"^[0-9][150][ -]([A-Z][ -][0-9]{3}[ -][A-Z]{2})|([0-9]{3}[ -][A-Z]{3})$"))
async def set_cat(mes: Message, state: FSMContext):
    data = {'nomeri': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    await mes.answer(f"Moshinangiz raqami <b>{res['nomeri']}</b> ga o'zgartirildi!", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(content_types=['text'], state=EditInstructor.moshina)
async def set_cat(mes: Message, state: FSMContext):
    data = {'moshina': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    await mes.answer(f"Moshinangiz <b>{res['moshina']}</b> ga o'zgartirildi!", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(text="Darslar ro'yxati")
async def get_sessions(mes: Message):
    await mes.answer("Darslar ro'yxatini tanlang👇", reply_markup=sessions)
