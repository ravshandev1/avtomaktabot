from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery
import requests
from data.config import BASE_URL
from states.instructor import DeleteIns
from states.instructor import InstructorForm, EditInstructor
from aiogram.dispatcher import FSMContext
from loader import dp
from keyboards.default.register import genders, regions, categories, card_btn, text_ins_reg, text_ins_up
from keyboards.default.is_authenticated import menu_instructor, location_btn, profile_delete
from keyboards.inline.edit_profile import instructor
from keyboards.inline.sessions import sessions
import re


@dp.message_handler(text='Инструктор')
async def register(mes: Message):
    await InstructorForm.ism.set()
    await mes.answer(text_ins_reg()['ism'], reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=InstructorForm.ism)
async def ism(mes: Message, state: FSMContext):
    await state.update_data(
        {"ism": mes.text}
    )
    await mes.answer(text_ins_reg()['familiya'])
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.familiya)
async def familiya(mes: Message, state: FSMContext):
    await state.update_data(
        {'familiya': mes.text}
    )
    await mes.answer(text_ins_reg()['telefon'])
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.telefon, regexp=re.compile(r"^[378]{2}|9[01345789]\d{7}$"))
async def telefon(mes: Message, state: FSMContext):
    await state.update_data(
        {'telefon': f"998{mes.text}"}
    )
    await mes.answer(text_ins_reg()['jins'], reply_markup=genders)
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.telefon, content_types='text')
async def st(mes: Message):
    await mes.answer(text_ins_reg()['telefon_qayta'])
    await InstructorForm.telefon.set()


@dp.message_handler(state=InstructorForm.jins)
async def gender(mes: Message, state: FSMContext):
    await state.update_data(
        {'jins': mes.text}
    )
    await mes.answer(text_ins_reg()['manzil'], reply_markup=regions())
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.tuman)
async def region(mes: Message, state: FSMContext):
    await state.update_data(
        {'tuman': mes.text}
    )
    await mes.answer(text_ins_reg()['categoriya'], reply_markup=categories())
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
    await mes.answer(text_ins_reg()['moshina'], reply_markup=markup)
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.moshina)
async def car(mes: Message, state: FSMContext):
    await state.update_data(
        {'moshina': mes.text}
    )
    await mes.answer(text_ins_reg()['moshina_nomeri'], reply_markup=ReplyKeyboardRemove())
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.nomeri, regexp=re.compile(
    r"^[0-9][150][ -]([A-Z][ -][0-9]{3}[ -][A-Z]{2})|([0-9]{3}[ -][A-Z]{3})$"))
async def create_instructor(mes: Message, state: FSMContext):
    await state.update_data(
        {'nomeri': mes.text, 'telegram_id': mes.from_user.id}
    )
    await mes.answer(text_ins_reg()['karta'], reply_markup=card_btn)
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.card)
async def card(mes: Message, state: FSMContext):
    await state.update_data(
        {'card': mes.text}
    )
    await mes.answer(text_ins_reg()['lacatsiya'], reply_markup=location_btn)
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.location, content_types='location')
async def get_location(mes: Message, state: FSMContext):
    data = await state.get_data()
    data['location'] = f"{mes.location['latitude']}, {mes.location['longitude']}"
    res = requests.post(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    r = res.json()
    await mes.answer(f"{mes.from_user.first_name} {r['message']}", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(state=InstructorForm.nomeri, content_types='text')
async def st(mes: Message):
    await mes.answer(text_ins_reg()['moshina_nomeri_qayta'])
    await InstructorForm.nomeri.set()


# @dp.message_handler(text="Бот ҳисобингиздан оладиган хизмат ҳақи")
# async def price(mes: Message):
#     r1 = requests.get(url=f"{BASE_URL}/session/percent/")
#     p1 = r1.json()
#     text = ""
#     for j in p1:
#         text += f"Машғулотнинг умумий суммасидан бот <b>{j['percent']}</b> % олади\n"
#     await mes.answer(text)


@dp.message_handler(text="👨‍✈️️Профил")
async def get_profile(mes: Message):
    rp = requests.get(url=f"{BASE_URL}/instructor/{mes.from_user.id}/")
    res = rp.json()
    text = f"Исмингиз: <b>{res['ism']}</b>\n"
    text += f"Фамилиянгиз: <b>{res['familiya']}</b>\n"
    text += f"Телефон рақамангиз: <b>{res['telefon']}</b>\n"
    text += f"Мошинагиз: <b>{res['moshina']}</b>\n"
    text += f"Яшаш туманингиз: <b>{res['tuman']}</b>\n"
    text += f"Тоифангиз: <b>{res['toifa_name']}</b>\n"
    # text += f"Балансизгиз: <b>{res['balans']} so'm</b>\n"
    text += f"Мошинангиз номери: <b>{res['nomeri']}</b>\n"
    await mes.answer(text, reply_markup=menu_instructor)


@dp.message_handler(text="👨‍✈️Профилни ўзгартириш")
async def edit_profile(mes: Message):
    await mes.answer("Нимани ўзгартирмоқчисиз?", reply_markup=instructor)


@dp.message_handler(text="👨‍✈️Профилни ўчириш")
async def a(mes: Message):
    await mes.answer('Профилингизни ўчирмоқчимисиз?', reply_markup=profile_delete)
    await DeleteIns.yes_or_no.set()


@dp.message_handler(state=DeleteIns.yes_or_no)
async def delete_profile(mes: Message, state: FSMContext):
    if mes.text == 'Ҳа':
        rp = requests.delete(url=f"{BASE_URL}/client/delete/{mes.from_user.id}/")
        if rp.status_code == 204:
            await mes.answer("Профилингиз ўчирилди", reply_markup=ReplyKeyboardRemove())
        else:
            await mes.answer("Нимадир хато кетди қайтадан ўриниб кўринг!")
    elif mes.text == 'Йўқ':
        await mes.answer("Керакли булимни танланг 👇", reply_markup=menu_instructor)
    await state.finish()


@dp.callback_query_handler(
    text=['instructor:name', 'instructor:surname', 'instructor:phone', 'car', 'number', 'region', 'cat', 'locate',
          'cart'])
async def set_state(call: CallbackQuery):
    if call.data == "instructor:name":
        await call.message.answer(text_ins_up()['ism'])
        await EditInstructor.ism.set()
    elif call.data == "instructor:surname":
        await call.message.answer(text_ins_up()['familiya'])
        await EditInstructor.familiya.set()
    elif call.data == "instructor:phone":
        await call.message.answer(text_ins_up()['telefon'])
        await EditInstructor.telefon.set()
    elif call.data == "car":
        res = requests.get(url=f"{BASE_URL}/instructor/cars/")
        rg = res.json()
        markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
        for i in rg:
            markup.insert(KeyboardButton(text=f"{i['nomi']}"))
        await call.message.answer(text_ins_up()['moshina'], reply_markup=markup)
        await EditInstructor.moshina.set()
    elif call.data == "region":
        await call.message.answer(text_ins_up()['manzil'], reply_markup=regions())
        await EditInstructor.tuman.set()
    elif call.data == 'cat':
        await call.message.answer(text_ins_up()['categoriya'], reply_markup=categories())
        await EditInstructor.toifa.set()
    elif call.data == "number":
        await call.message.answer(text_ins_up()['moshina_nomeri'])
        await EditInstructor.nomeri.set()
    elif call.data == "locate":
        await call.message.answer(text_ins_up()['lacatsiya'], reply_markup=location_btn)
        await EditInstructor.location.set()
    elif call.data == "cart":
        await call.message.answer(text_ins_up()['karta'], reply_markup=card_btn)
        await EditInstructor.card.set()
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


@dp.message_handler(regexp=re.compile(r"^[378]{2}|9[01345789]\d{7}$"), state=EditInstructor.telefon)
async def set_phone(mes: Message, state: FSMContext):
    data = {'telefon': f"998{mes.text}"}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    await mes.answer(f"Телефонгиз <b>{res['telefon']}</b> га ўзгартирилди!", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(state=EditInstructor.telefon, content_types=['text'])
async def a(mes: Message):
    await mes.answer(text_ins_up()['telefon_qayta'])
    await EditInstructor.telefon.set()


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
    await mes.answer(f"Тоифанингиз <b>{res['toifa_name']}</b> га ўзгартирилди!", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(state=EditInstructor.nomeri, regexp=re.compile(
    r"^[0-9][150][ -]([A-Z][ -][0-9]{3}[ -][A-Z]{2})|([0-9]{3}[ -][A-Z]{3})$"))
async def set_cat(mes: Message, state: FSMContext):
    data = {'nomeri': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    await mes.answer(f"Мошинангиз рақами <b>{res['nomeri']}</b> га ўзгартирилди!", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(state=EditInstructor.nomeri, content_types=['text'])
async def a(mes: Message):
    await mes.answer(text_ins_up()['moshina_nomeri_qayta'])
    await EditInstructor.nomeri.set()


@dp.message_handler(content_types=['text'], state=EditInstructor.moshina)
async def set_cat(mes: Message, state: FSMContext):
    data = {'moshina': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    await mes.answer(f"Мошинангиз <b>{res['moshina']}</b> га ўзгартирилди!", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(content_types=['text'], state=EditInstructor.card)
async def set_cat(mes: Message, state: FSMContext):
    data = {'card': mes.text}
    requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    await mes.answer(f"Тўлов тури ўзгартирилди!", reply_markup=menu_instructor)
    await state.finish()


@dp.message_handler(text="👨‍✈️Машғулотлар рўйхати")
async def get_sessions(mes: Message):
    await mes.answer("Машғулотлар рўйхатини танланг👇", reply_markup=sessions)
