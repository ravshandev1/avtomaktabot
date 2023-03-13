from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery
import requests
from data.config import BASE_URL
from states.instructor import InstructorForm, EditInstructor
from aiogram.dispatcher import FSMContext
from loader import dp
from keyboards.default.register import genders, regions, categories
from keyboards.default.is_authenticated import menu_instructor, location_btn
from keyboards.inline.edit_profile import instructor
from keyboards.inline.sessions import sessions
import re


@dp.message_handler(text='Инструктор')
async def register(mes: Message):
    await InstructorForm.ism.set()
    await mes.answer("Исмингиз:", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=InstructorForm.ism)
async def ism(mes: Message, state: FSMContext):
    await state.update_data(
        {"ism": mes.text}
    )
    await mes.answer("Фамилиянгиз:")
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.familiya)
async def familiya(mes: Message, state: FSMContext):
    await state.update_data(
        {'familiya': mes.text}
    )
    await mes.answer(
        'Телефон рақамингизни коди билан 7 та рақмини қўшиб ёзинг\nМасалан: <b>901234567</b> кўришнишда ёзинг')
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.telefon, regexp=re.compile(r"^[378]{2}|9[01345789]\d{7}$"))
async def telefon(mes: Message, state: FSMContext):
    await state.update_data(
        {'telefon': f"998{mes.text}"}
    )
    await mes.answer("Жинсингиз: ", reply_markup=genders)
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.telefon, content_types='text')
async def st(mes: Message):
    await mes.answer("Телефон рақамни нотўғри киритдингиз!\nТелефон рақамингизни қайтадан киритинг!")
    await InstructorForm.telefon.set()


@dp.message_handler(state=InstructorForm.jins)
async def gender(mes: Message, state: FSMContext):
    await state.update_data(
        {'jins': mes.text}
    )
    await mes.answer("Яшаш туманингиз: ", reply_markup=regions())
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.tuman)
async def region(mes: Message, state: FSMContext):
    await state.update_data(
        {'tuman': mes.text}
    )
    await mes.answer("Қайси тоифа инструктирисиз: ", reply_markup=categories())
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
    await mes.answer("Машинани танланг: ", reply_markup=markup)
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.moshina)
async def car(mes: Message, state: FSMContext):
    await state.update_data(
        {'moshina': mes.text}
    )
    await mes.answer(
        "Мошинангиз номерини ёзинг\nМасалан: <b>01 A 111 AA</b> ёки <b>01 111 AAA</b> кўринишида булсин",
        reply_markup=ReplyKeyboardRemove())
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.nomeri, regexp=re.compile(
    r"^[0-9][150][ -]([A-Z][ -][0-9]{3}[ -][A-Z]{2})|([0-9]{3}[ -][A-Z]{3})$"))
async def create_instructor(mes: Message, state: FSMContext):
    await state.update_data(
        {'nomeri': mes.text, 'telegram_id': mes.from_user.id}
    )
    await mes.answer("Ўзингизга қулай бўлган манзилни юборинг!", reply_markup=location_btn)
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.nomeri, content_types='text')
async def st(mes: Message):
    await mes.answer(
        "Мошина рақамни нотўғри киритдингиз!\nҚайтадан киритинг\nМасалан: <b>01 A 111 AA</b> ёки <b>01 111 AAA</b> кўринишида булсин")
    await InstructorForm.nomeri.set()


@dp.message_handler(text="Нарх")
async def price(mes: Message):
    r = requests.get(url=f"{BASE_URL}/session/price/list/")
    pr = r.json()
    text = ""
    for i in pr:
        text += f"{i['category']} тоифа - {i['price']} сўм соатига\n"
    await mes.answer(text)


@dp.message_handler(text="Фоиз")
async def price(mes: Message):
    r1 = requests.get(url=f"{BASE_URL}/session/percent/")
    p1 = r1.json()
    text = ""
    for j in p1:
        text += f"Инструктордан олинадиган фоизи {j['percent']} %\n"
    await mes.answer(text)


@dp.message_handler(state=InstructorForm.location, content_types='location')
async def get_location(mes: Message, state: FSMContext):
    data = await state.get_data()
    data['location'] = f"{mes.location['longitude']}, {mes.location['latitude']}"
    res = requests.post(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    r = res.json()
    await mes.answer(f"{mes.from_user.first_name} {r['message']}", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(text="🧑‍✈️Профил")
async def get_profile(mes: Message):
    rp = requests.get(url=f"{BASE_URL}/instructor/{mes.from_user.id}/")
    res = rp.json()
    text = f"Исмингиз: <b>{res['ism']}</b>\n"
    text += f"Фамилиянгиз: <b>{res['familiya']}</b>\n"
    text += f"Телефон рақамангиз: <b>{res['telefon']}</b>\n"
    text += f"Мошинагиз: <b>{res['moshina']}</b>\n"
    text += f"Яшаш туманингиз: <b>{res['tuman']}</b>\n"
    text += f"Тоифангиз: <b>{res['toifa']}</b>\n"
    text += f"Балансизгиз: <b>{res['balans']} so'm</b>\n"
    text += f"Мошинангиз номери: <b>{res['nomeri']}</b>\n"
    await mes.answer(text, reply_markup=menu_instructor)


@dp.message_handler(text="🧑‍✈️Профилни ўзгартириш")
async def edit_profile(mes: Message):
    await mes.answer("Нимани ўзгартирмоқчисиз?", reply_markup=instructor)


@dp.callback_query_handler(
    text=['instructor:name', 'instructor:surname', 'instructor:phone', 'car', 'number', 'region', 'cat', 'locate'])
async def set_state(call: CallbackQuery):
    if call.data == "instructor:name":
        await call.message.answer("Исмингизни ёзинг:")
        await EditInstructor.ism.set()
    elif call.data == "instructor:surname":
        await call.message.answer("Фамилиянгизни ёзинг:")
        await EditInstructor.familiya.set()
    elif call.data == "instructor:phone":
        await call.message.answer(
            "Телефон рақамингизни коди билан 7 та рақмини қўшиб ёзинг\nМасалан: <b>901234567</b> кўришнишда ёзинг")
        await EditInstructor.telefon.set()
    elif call.data == "car":
        res = requests.get(url=f"{BASE_URL}/instructor/cars/")
        rg = res.json()
        markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
        for i in rg:
            markup.insert(KeyboardButton(text=f"{i['nomi']}"))
        await call.message.answer("Мошина номини танланг:", reply_markup=markup)
        await EditInstructor.moshina.set()
    elif call.data == "region":
        await call.message.answer("Яшаш манзилингизни танланг", reply_markup=regions())
        await EditInstructor.tuman.set()
    elif call.data == 'cat':
        await call.message.answer("Тоифани танланг:", reply_markup=categories())
        await EditInstructor.toifa.set()
    elif call.data == "number":
        await call.message.answer(
            "Мошинангиз номерини ёзинг\nМасалан: <b>01 A 111 AA</b> ёки <b>01 111 AAA</b> кўринишида булсин")
        await EditInstructor.nomeri.set()
    elif call.data == "locate":
        await call.message.answer(
            "Манзилингизни юборинг!", reply_markup=location_btn)
        await EditInstructor.location.set()
    await call.answer(cache_time=3)


@dp.message_handler(content_types=['text'], state=EditInstructor.ism)
async def set_name(mes: Message, state: FSMContext):
    data = {'ism': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    await mes.answer(f"Исмингиз <b>{res['ism']}</b> га ўзгартирилди!", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(content_types=['text'], state=EditInstructor.familiya)
async def set_surname(mes: Message, state: FSMContext):
    data = {'familiya': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    await mes.answer(f"Фамилиянгиз <b>{res['familiya']}</b> га ўзгартирилди!", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(content_types='location', state=EditInstructor.location)
async def set_surname(mes: Message, state: FSMContext):
    data = {'location': f"{mes.location['latitude']}, {mes.location['longitude']}"}
    requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    await mes.answer(f"Манзилингиз ўзгартирилди!", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(content_types=['text'], state=EditInstructor.telefon)
async def set_phone(mes: Message, state: FSMContext):
    data = {'telefon': f"998{mes.text}"}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    await mes.answer(f"Телефонгиз <b>{res['telefon']}</b> га ўзгартирилди!", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(content_types=['text'], state=EditInstructor.tuman)
async def set_region(mes: Message, state: FSMContext):
    data = {'tuman': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    await mes.answer(f"Яшаш туманингиз <b>{res['tuman']}</b> га ўзгартирилди!", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(content_types=['text'], state=EditInstructor.toifa)
async def set_cat(mes: Message, state: FSMContext):
    data = {'toifa': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    await mes.answer(f"Тоифанингиз <b>{res['toifa']}</b> га ўзгартирилди!", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(content_types=['text'], state=EditInstructor.nomeri, regexp=re.compile(
    r"^[0-9][150][ -]([A-Z][ -][0-9]{3}[ -][A-Z]{2})|([0-9]{3}[ -][A-Z]{3})$"))
async def set_cat(mes: Message, state: FSMContext):
    data = {'nomeri': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    await mes.answer(f"Мошинангиз рақами <b>{res['nomeri']}</b> га ўзгартирилди!", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(content_types=['text'], state=EditInstructor.moshina)
async def set_cat(mes: Message, state: FSMContext):
    data = {'moshina': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    await mes.answer(f"Мошинангиз <b>{res['moshina']}</b> га ўзгартирилди!", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(text="🧑‍✈️Машғулотлар рўйхати")
async def get_sessions(mes: Message):
    await mes.answer("Машғулотлар рўйхатини танланг👇", reply_markup=sessions)
