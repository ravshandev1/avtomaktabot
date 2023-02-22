from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
import requests
import re
from data.config import BASE_URL
from states.client import ClientForm, EditClient
from aiogram.dispatcher import FSMContext
from loader import dp
from keyboards.default.register import prava
from keyboards.inline.edit_profile import client
from keyboards.default.is_authenticated import menu_client, action_session, sessions, edit_session
from keyboards.inline.sessions import create_after_sessions_for_cl, before_sessions_for_cl


@dp.message_handler(text='Client')
async def register(mes: Message):
    await mes.answer('Ismingiz: ', reply_markup=ReplyKeyboardRemove())
    await ClientForm.ism.set()


@dp.message_handler(state=ClientForm.ism)
async def name(mes: Message, state: FSMContext):
    await state.update_data(
        {'ism': mes.text}
    )
    await mes.answer("Familiyangiz:")
    await ClientForm.next()


@dp.message_handler(state=ClientForm.familiya)
async def surname(mes: Message, state: FSMContext):
    await state.update_data(
        {"familiya": mes.text}
    )
    await mes.answer(
        'Telefon raqamingizni kodi bilan 7 ta raqmini qushib yozing\nMasalan: <b>901234567</b> kurishnishda yozing')
    await ClientForm.next()


@dp.message_handler(state=ClientForm.telefon, regexp=re.compile(r"^[378]{2}|9[01345789]\d{7}$"))
async def get_phone(mes: Message, state: FSMContext):
    await state.update_data(
        {'telefon': f"998{mes.text}"}
    )
    await mes.answer('Pravaningiz bormi?', reply_markup=prava)
    await ClientForm.next()


@dp.message_handler(state=ClientForm.prava)
async def get_cat(mes: Message, state: FSMContext):
    await state.update_data(
        {"prava": mes.text, "telegram_id": mes.from_user.id}
    )
    data = await state.get_data()
    res = requests.post(url=f"{BASE_URL}/client/{mes.from_user.id}/", data=data)
    text = res.json()
    await mes.answer(f"{data['ism']} {text['message']}", reply_markup=menu_client)
    await state.finish()


@dp.message_handler(text="Profile")
async def get_profile(mes: Message):
    rp = requests.get(url=f"{BASE_URL}/client/{mes.from_user.id}/")
    res = rp.json()
    text = f"Ismingiz: <b>{res['ism']}</b>\n"
    text += f"Familiyangiz: <b>{res['familiya']}</b>\n"
    text += f"Telefon raqamangiz: <b>{res['telefon']}</b>\n"
    text += f"Pravangiz: <b>{res['prava']}</b>"
    await mes.answer(text, reply_markup=menu_client)


@dp.message_handler(text="Profileni o'zgartirish")
async def edit_profile(mes: Message):
    await mes.answer("Nimani o'zgartirmoqchisiz?", reply_markup=client)


@dp.callback_query_handler(text=['client:name', 'client:surname', 'client:phone', 'pra'])
async def set_state(call: CallbackQuery):
    if call.data == 'client:name':
        await call.message.answer("Ismingizni yozing:")
        await EditClient.ism.set()
    elif call.data == 'client:surname':
        await call.message.answer("Familiyangizni yozing:")
        await EditClient.familiya.set()
    elif call.data == 'client:phone':
        await call.message.answer(
            "Telefon raqamingizni kodi bilan 7 ta raqmini qushib yozing\nMasalan: <b>901234567</b> kurishnishda yozing")
        await EditClient.telefon.set()
    elif call.data == 'pra':
        await call.message.answer("Prava oldingizmi?", reply_markup=prava)
        await EditClient.prava.set()
    await call.answer(cache_time=3)


@dp.message_handler(content_types=['text'], state=EditClient.ism)
async def set_name(mes: Message, state: FSMContext):
    data = {'ism': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/client/{mes.from_user.id}/", data=data)
    res = rp.json()
    await mes.answer(f"Ismingiz {res['ism']} ga o'zgartirildi!", reply_markup=menu_client)
    await state.finish()


@dp.message_handler(content_types=['text'], state=EditClient.familiya)
async def set_surname(mes: Message, state: FSMContext):
    data = {'familiya': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/client/{mes.from_user.id}/", data=data)
    res = rp.json()
    await mes.answer(f"Familiyangiz {res['familiya']} ga o'zgartirildi!", reply_markup=menu_client)
    await state.finish()


@dp.message_handler(content_types=['text'], state=EditClient.telefon)
async def set_phone(mes: Message, state: FSMContext):
    data = {'telefon': f"998{mes.text}"}
    rp = requests.patch(url=f"{BASE_URL}/client/{mes.from_user.id}/", data=data)
    res = rp.json()
    await mes.answer(f"Telefongiz {res['telefon']} ga o'zgartirildi!", reply_markup=menu_client)
    await state.finish()


@dp.message_handler(content_types=['text'], state=EditClient.prava)
async def set_cat(mes: Message, state: FSMContext):
    data = {'prava': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/client/{mes.from_user.id}/", data=data)
    res = rp.json()
    await mes.answer(f"Pravangiz {res['prava']} ga o'zgartirildi!", reply_markup=menu_client)
    await state.finish()


@dp.message_handler(text='Session')
async def ses(mes: Message):
    await mes.answer("Kerakli bo'limni tanlang 👇", reply_markup=action_session)


@dp.message_handler(text='⬅️Ortga')
async def ses(mes: Message):
    await mes.answer("Kerakli bo'limni tanlang 👇", reply_markup=action_session)


@dp.message_handler(text="Sessionlar ro'yxati")
async def session(mes: Message):
    await mes.answer("Darslar ro'yxatini tanlang👇", reply_markup=sessions)


@dp.message_handler(text="Bo'lishi kerak")
async def lesson(mes: Message):
    rp = requests.get(url=f"{BASE_URL}/session/{mes.from_user.id}")
    res = rp.json()
    row = ""
    for (i, se) in zip(range(1, 6), res['results']):
        row += f"{i}.{se['instructor']} {se['moshina']} {se['vaqt']}\n     {se['i_telefoni']}\n"
    await mes.answer(f"Natija {res['count']} ta\n" + row,
                     reply_markup=create_after_sessions_for_cl(res, page=1))


@dp.message_handler(text="Bo'lib o'tgan")
async def lesson(mes: Message):
    rp = requests.get(url=f"{BASE_URL}/session/finished/{mes.from_user.id}")
    res = rp.json()
    row = ""
    for (i, se) in zip(range(1, 6), res['results']):
        row += f"{i}.{se['instructor']} {se['moshina']} {se['vaqt']}\n     {se['i_telefoni']}\n"
    await mes.answer(f"Natija {res['count']} ta\n" + row,
                     reply_markup=before_sessions_for_cl(page=1))


@dp.callback_query_handler(text_contains='rav')
async def action(call: CallbackQuery):
    page = int(call.data.split('rav:')[1])
    r = requests.get(url=f"{BASE_URL}/session/{call.from_user.id}/?page={page}")
    res = r.json()
    if res['next']:
        r1 = requests.get(url=f"{BASE_URL}/session/{call.from_user.id}/?page={page + 1}")
        res = r1.json()
        row = ""
        for (i, se) in zip(range(1, 6), res['results']):
            row += f"{i}.{se['instructor']} {se['moshina']} {se['vaqt']}\n     {se['i_telefoni']}\n"
        await call.message.edit_text(f"Natija {res['count']} ta\n" + row,
                                     reply_markup=create_after_sessions_for_cl(res, page + 1))
    else:
        await call.answer("Bu oxirgi saxifa!")
    await call.answer(cache_time=3)


@dp.callback_query_handler(text_contains='bob')
async def action(call: CallbackQuery):
    page = int(call.data.split('bob:')[1])
    r = requests.get(url=f"{BASE_URL}/session/{call.from_user.id}/?page={page}")
    res = r.json()
    if res['previous']:
        r1 = requests.get(url=f"{BASE_URL}/session/{call.from_user.id}/?page={page - 1}")
        res = r1.json()
        row = ""
        for (i, se) in zip(range(1, 6), res['results']):
            row += f"{i}.{se['instructor']} {se['moshina']} {se['vaqt']}\n     {se['i_telefoni']}\n"
        await call.message.edit_text(f"Natija {res['count']} ta\n" + row,
                                     reply_markup=create_after_sessions_for_cl(res, page - 1))
    else:
        await call.answer("Bu birinchi saxifa!")
    await call.answer(cache_time=3)


@dp.callback_query_handler(text_contains='kam')
async def action(call: CallbackQuery):
    page = int(call.data.split('kam:')[1])
    r = requests.get(url=f"{BASE_URL}/session/finished/{call.from_user.id}/?page={page}")
    res = r.json()
    if res['next']:
        r1 = requests.get(url=f"{BASE_URL}/session/finished/{call.from_user.id}/?page={page + 1}")
        res = r1.json()
        row_2 = ""
        for (i, se) in zip(range(1, 6), res['results']):
            row_2 += f"{i}.{se['instructor']} {se['moshina']} {se['vaqt']}\n     {se['i_telefoni']}\n"
        await call.message.edit_text(f"Natija {res['count']} ta\n" + row_2,
                                     reply_markup=before_sessions_for_cl(page + 1))
    else:
        await call.answer("Bu oxirgi saxifa!")
    await call.answer(cache_time=3)


@dp.callback_query_handler(text_contains='jal')
async def action(call: CallbackQuery):
    page = int(call.data.split('jal:')[1])
    r = requests.get(url=f"{BASE_URL}/session/finished/{call.from_user.id}/?page={page}")
    res = r.json()
    if res['previous']:
        r1 = requests.get(url=f"{BASE_URL}/session/finished/{call.from_user.id}/?page={page - 1}")
        res = r1.json()
        row_2 = ""
        for (i, se) in zip(range(1, 6), res['results']):
            row_2 += f"{i}.{se['instructor']} {se['moshina']} {se['vaqt']}\n     {se['i_telefoni']}\n"
        await call.message.edit_text(f"Natija {res['count']} ta\n" + row_2,
                                     reply_markup=before_sessions_for_cl(page - 1))
    else:
        await call.answer("Bu birinchi saxifa!")
    await call.answer(cache_time=3)


@dp.callback_query_handler(text_contains='scl:')
async def daa(call: CallbackQuery, state: FSMContext):
    s_id = call.data.split('scl:')[1]
    await state.update_data(
        {'session_id': s_id}
    )
    await call.message.answer("Nimani o'zgartirmoqchisiz?", reply_markup=edit_session)


@dp.message_handler(text='Sessionni o\'chirish')
async def delete(mes: Message, state: FSMContext):
    s_id = await state.get_data()
    rp = requests.delete(url=f"{BASE_URL}/session/detail/{s_id['session_id']}/")
    if rp.status_code == 204:
        await mes.answer("Session muvaffaqiyatli o'chirildi", reply_markup=menu_client)
    else:
        await mes.answer("Nimadir xato ketdi boshqatdan o'rinib ko'ring!")


@dp.message_handler(text="Bosh menu")
async def menu(mes: Message):
    await mes.answer("Kerakli bo'limni tanlang 👇", reply_markup=menu_client)


@dp.message_handler(text="Profileni o'chirish")
async def delete_profile(mes: Message):
    rp = requests.delete(url=f"{BASE_URL}/client/delete/{mes.from_user.id}/")
    if rp.status_code == 204:
        await mes.answer("Profilingiz muvaffaqiyatli o'chirildi", reply_markup=ReplyKeyboardRemove())
    else:
        await mes.answer("Nimadir xato ketdi qaytadan o'rinib ko'ring!")


@dp.callback_query_handler(text=['juda_yomon', 'yomon', 'qoniqarli', 'yaxshi', 'zur'])
async def rate(call: CallbackQuery):
    rt = 0
    if call.data == 'juda_yomon':
        rt = 1
    elif call.data == 'yomon':
        rt = 2
    elif call.data == 'qoniqarli':
        rt = 3
    elif call.data == 'yaxshi':
        rt = 4
    elif call.data == 'zur':
        rt = 5
    rp = requests.patch(url=f"{BASE_URL}/instructor/rating/",
                        data={'client': call.from_user.id, 'rate': rt})
    res = rp.json()
    await call.message.answer(f"{res['message']}", reply_markup=menu_client)
    await call.answer(cache_time=3)
