from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
import requests
import re
from data.config import BASE_URL
from states.client import ClientForm, EditClient, DeleteCl
from aiogram.dispatcher import FSMContext
from loader import dp
from keyboards.default.register import prava, text_client_reg, text_client_up
from keyboards.inline.edit_profile import client
from keyboards.default.is_authenticated import menu_client, action_session, sessions, edit_session, profile_delete
from keyboards.inline.sessions import create_after_sessions_for_cl, before_sessions_for_cl
from utils.notify_admins import notify_session_deleted

lang = ''


@dp.message_handler(text=['Ўрганувчи', 'Ученик'])
async def register(mes: Message):
    global lang
    if mes.text == 'Ученик':
        lang = 'ru'
        await mes.answer(text_client_reg()['ism_ru'], reply_markup=ReplyKeyboardRemove())
    else:
        lang = 'uz'
        await mes.answer(text_client_reg()['ism'], reply_markup=ReplyKeyboardRemove())
    await ClientForm.ism.set()


@dp.message_handler(state=ClientForm.ism)
async def name(mes: Message, state: FSMContext):
    await state.update_data(
        {'ism': mes.text}
    )
    if lang == 'uz':
        await mes.answer(text_client_reg()['familiya'])
    elif lang == 'ru':
        await mes.answer(text_client_reg()['familiya_ru'])
    await ClientForm.next()


@dp.message_handler(state=ClientForm.familiya)
async def surname(mes: Message, state: FSMContext):
    await state.update_data(
        {"familiya": mes.text}
    )
    if lang == 'uz':
        await mes.answer(text_client_reg()['telefon'])
    else:
        await mes.answer(text_client_reg()['telefon_ru'])
    await ClientForm.next()


@dp.message_handler(state=ClientForm.telefon, regexp=re.compile(r"^[378]{2}|9[01345789]\d{7}$"))
async def get_phone(mes: Message, state: FSMContext):
    await state.update_data(
        {'telefon': f"998{mes.text}"}
    )
    if lang == 'uz':
        await mes.answer(text_client_reg()['prava'], reply_markup=prava(lang))
    else:
        await mes.answer(text_client_reg()['prava_ru'], reply_markup=prava(lang))
    await ClientForm.next()


@dp.message_handler(state=ClientForm.telefon, content_types='text')
async def st(mes: Message):
    if lang == 'uz':
        await mes.answer(text_client_reg()['telefon_qayta'])
    else:
        await mes.answer(text_client_reg()['telefon_qayta_ru'])
    await ClientForm.telefon.set()


@dp.message_handler(state=ClientForm.prava)
async def get_cat(mes: Message, state: FSMContext):
    await state.update_data(
        {"prava": mes.text, "telegram_id": mes.from_user.id}
    )
    data = await state.get_data()
    res = requests.post(url=f"{BASE_URL}/client/{mes.from_user.id}/", data=data)
    text = res.json()
    await mes.answer(f"{data['ism']} {text['message']}\n", reply_markup=menu_client(lang))
    if (mes.text == 'Бор') or (mes.text == 'Есть'):
        if lang == 'uz':
            await mes.answer(text_client_reg()['prava_bor'])
        else:
            await mes.answer(text_client_reg()['prava_bor_ru'])
    else:
        if lang == 'uz':
            await mes.answer(text_client_reg()['prava_yuq'])
        else:
            await mes.answer(text_client_reg()['prava_yuq_ru'])
    await state.finish()


@dp.message_handler(text=["Профил", "Профиль"])
async def get_profile(mes: Message):
    rp = requests.get(url=f"{BASE_URL}/client/{mes.from_user.id}/")
    res = rp.json()
    if lang == 'uz':
        text = f"Исмингиз: <b>{res['ism']}</b>\n"
        text += f"Фамилиянгиз: <b>{res['familiya']}</b>\n"
        text += f"Телефон рақамингиз: <b>{res['telefon']}</b>\n"
        text += f"Ҳайдовчилик гувоҳномангиз: <b>{res['prava']}</b>"
    else:
        text = f"Ваше имя: <b>{res['ism']}</b>\n"
        text += f"Ваша фамилия: <b>{res['familiya']}</b>\n"
        text += f"Ваш номер телефона: <b>{res['telefon']}</b>\n"
        text += f"Ваши водительские права: <b>{res['prava']}</b>"
    await mes.answer(text, reply_markup=menu_client(lang))


@dp.message_handler(text=["Профилни ўзгартириш", "Изменение профиля"])
async def edit_profile(mes: Message):
    if lang == 'uz':
        await mes.answer("Нимани ўзгартирмоқчисиз?", reply_markup=client(lang))
    else:
        await mes.answer("Что вы хотите изменить?", reply_markup=client(lang))


@dp.callback_query_handler(text=['client:name', 'client:surname', 'client:phone', 'pra'])
async def set_state(call: CallbackQuery):
    if call.data == 'client:name':
        if lang == 'uz':
            await call.message.answer(text_client_up()['ism'])
        else:
            await call.message.answer(text_client_up()['ism_ru'])
        await EditClient.ism.set()
    elif call.data == 'client:surname':
        if lang == 'uz':
            await call.message.answer(text_client_up()['familiya'])
        else:
            await call.message.answer(text_client_up()['familiya_ru'])
        await EditClient.familiya.set()
    elif call.data == 'client:phone':
        if lang == 'uz':
            await call.message.answer(text_client_up()['telefon'])
        else:
            await call.message.answer(text_client_up()['telefon_ru'])
        await EditClient.telefon.set()
    elif call.data == 'pra':
        if lang == 'uz':
            await call.message.answer(text_client_up()['prava'], reply_markup=prava(lang))
        else:
            await call.message.answer(text_client_up()['prava_ru'], reply_markup=prava(lang))
        await EditClient.prava.set()
    await call.answer(cache_time=3)


@dp.message_handler(content_types=['text'], state=EditClient.ism)
async def set_name(mes: Message, state: FSMContext):
    data = {'ism': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/client/{mes.from_user.id}/", data=data)
    res = rp.json()
    if lang == 'uz':
        await mes.answer(f"Исмингиз {res['ism']} га ўзгартирилди!", reply_markup=menu_client(lang))
    else:
        await mes.answer(f"Ваше имя изменён {res['ism']}", reply_markup=menu_client(lang))
    await state.finish()


@dp.message_handler(content_types=['text'], state=EditClient.familiya)
async def set_surname(mes: Message, state: FSMContext):
    data = {'familiya': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/client/{mes.from_user.id}/", data=data)
    res = rp.json()
    if lang == 'uz':
        await mes.answer(f"Фамилиянгиз {res['familiya']} га ўзгартирилди!", reply_markup=menu_client(lang))
    else:
        await mes.answer(f"Ваша фамилия изменён {res['familiya']}", reply_markup=menu_client(lang))
    await state.finish()


@dp.message_handler(regexp=re.compile(r"^[378]{2}|9[01345789]\d{7}$"), state=EditClient.telefon)
async def set_phone(mes: Message, state: FSMContext):
    data = {'telefon': f"998{mes.text}"}
    rp = requests.patch(url=f"{BASE_URL}/client/{mes.from_user.id}/", data=data)
    res = rp.json()
    if lang == 'uz':
        await mes.answer(f"Телефонингиз {res['telefon']} га ўзгартирилди!", reply_markup=menu_client(lang))
    else:
        await mes.answer(f"Твой телефон изменён {res['telefon']}", reply_markup=menu_client(lang))
    await state.finish()


@dp.message_handler(content_types=['text'], state=EditClient.telefon)
async def set_phone(mes: Message):
    if lang == 'uz':
        await mes.answer(text_client_up()['telefon_qayta'])
    else:
        await mes.answer(text_client_up()['telefon_qayta_ru'])
    await EditClient.telefon.set()


@dp.message_handler(content_types=['text'], state=EditClient.prava)
async def set_cat(mes: Message, state: FSMContext):
    data = {'prava': mes.text}
    requests.patch(url=f"{BASE_URL}/client/{mes.from_user.id}/", data=data)
    if lang == 'uz':
        await mes.answer(f"Ҳайдовчилик гувоҳномангиз ўзгартирилди!", reply_markup=menu_client(lang))
    else:
        await mes.answer(f"Ваши водительские права были изменены!", reply_markup=menu_client(lang))
    await state.finish()


@dp.message_handler(text=["Машғулот", "Тренировка"])
async def ses(mes: Message):
    if lang == 'uz':
        await mes.answer("Керакли бўлимни танланг 👇", reply_markup=action_session(lang))
    else:
        await mes.answer("Выберите нужный раздел 👇", reply_markup=action_session(lang))


@dp.message_handler(text=['⬅️Oртга', '⬅️Назад'])
async def ses(mes: Message):
    if lang == 'uz':
        await mes.answer("Керакли бўлимни танланг 👇", reply_markup=action_session(lang))
    else:
        await mes.answer("Выберите нужный раздел 👇", reply_markup=action_session(lang))


@dp.message_handler(text=["Машғулотлар рўйхати", "Список занятий"])
async def session(mes: Message):
    if lang == 'uz':
        await mes.answer("Машғулотлар рўйхатини танланг👇", reply_markup=sessions(lang))
    else:
        await mes.answer("Выберите список тренировок👇", reply_markup=sessions(lang))


@dp.message_handler(text=["Бўлиши керак", "Должен быть"])
async def lesson(mes: Message):
    rp = requests.get(url=f"{BASE_URL}/session/{mes.from_user.id}")
    res = rp.json()
    row = ""
    for (i, se) in zip(range(1, 6), res['results']):
        row += f"{i}. {se['instructor']} {se['moshina']} {se['vaqt']}\n     {se['i_telefoni']}\n"
    await mes.answer(f"Натижа {res['count']} та\n" + row,
                     reply_markup=create_after_sessions_for_cl(res, page=1))


@dp.message_handler(text=["Бўлиб утган", "Прошедший"])
async def lesson(mes: Message):
    rp = requests.get(url=f"{BASE_URL}/session/finished/{mes.from_user.id}")
    res = rp.json()
    row = ""
    for (i, se) in zip(range(1, 6), res['results']):
        row += f"{i}. {se['instructor']} {se['moshina']} {se['vaqt']}\n     {se['i_telefoni']}\n"
    await mes.answer(f"Натижа {res['count']} та\n" + row,
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
            row += f"{i}. {se['instructor']} {se['moshina']} {se['vaqt']}\n     {se['i_telefoni']}\n"
        await call.message.edit_text(f"Натижа {res['count']} тa\n" + row,
                                     reply_markup=create_after_sessions_for_cl(res, page + 1))
    else:
        if lang == 'uz':
            await call.answer("Бу охирги сахифа!")
        else:
            await call.answer("Это последняя страница!")
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
            row += f"{i}. {se['instructor']} {se['moshina']} {se['vaqt']}\n     {se['i_telefoni']}\n"
        await call.message.edit_text(f"Натижа {res['count']} тa\n" + row,
                                     reply_markup=create_after_sessions_for_cl(res, page - 1))
    else:
        if lang == 'uz':
            await call.answer("Бу биринчи сахифа!")
        else:
            await call.answer("Это первая страница!")
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
            row_2 += f"{i}. {se['instructor']} {se['moshina']} {se['vaqt']}\n     {se['i_telefoni']}\n"
        await call.message.edit_text(f"Натижа {res['count']} тa\n" + row_2,
                                     reply_markup=before_sessions_for_cl(page + 1))
    else:
        if lang == 'uz':
            await call.answer("Бу охирги сахифа!")
        else:
            await call.answer("Это последняя страница!")
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
            row_2 += f"{i}. {se['instructor']} {se['moshina']} {se['vaqt']}\n     {se['i_telefoni']}\n"
        await call.message.edit_text(f"Натижа {res['count']} тa\n" + row_2,
                                     reply_markup=before_sessions_for_cl(page - 1))
    else:
        if lang == 'uz':
            await call.answer("Бу биринчи сахифа!")
        else:
            await call.answer("Это первая страница!")
    await call.answer(cache_time=3)


@dp.callback_query_handler(text_contains='scl:')
async def daa(call: CallbackQuery, state: FSMContext):
    s_id = call.data.split('scl:')[1]
    await state.update_data(
        {'session_id': s_id}
    )
    if lang == 'uz':
        await call.message.answer("Керакли булимни танланг 👇", reply_markup=edit_session(lang))
    else:
        await call.message.answer("Выберите нужный раздел 👇", reply_markup=edit_session(lang))
    await call.answer(cache_time=1)


@dp.message_handler(text=['Машғулот манзилини олиш', "Получение адреса для обучения"])
async def delete(mes: Message, state: FSMContext):
    s_id = await state.get_data()
    rp = requests.get(url=f"{BASE_URL}/session/location/{s_id['session_id']}/")
    r = rp.json()
    await mes.answer_location(latitude=r['lat'], longitude=r['lon'])
    await state.finish()


@dp.message_handler(text=['Машғулотни бекор килиш', 'Отменить тренировку'])
async def delete(mes: Message, state: FSMContext):
    s_id = await state.get_data()
    rp = requests.delete(url=f"{BASE_URL}/session/detail/{s_id['session_id']}/")
    rs = rp.json()
    if rp.status_code == 200:
        if lang == 'uz':
            await mes.answer("Машғулот ўчирилди", reply_markup=menu_client(lang))
        else:
            await mes.answer("Тренировка удалена", reply_markup=menu_client(lang))
        await notify_session_deleted(instructor=rs['id1'], time=rs['vaqt'], lang=lang)
    else:
        if lang == 'uz':
            await mes.answer("Нимадир хато кетди бошқатдан ўриниб кўринг!")
        else:
            await mes.answer("Что-то пошло не так, попробуйте заменить другое!")
    await state.finish()


@dp.message_handler(text=["Бош меню", "Главное меню"])
async def menu(mes: Message):
    if lang == 'uz':
        await mes.answer("Керакли булимни танланг 👇", reply_markup=menu_client(lang))
    else:
        await mes.answer("Выберите нужный раздел 👇", reply_markup=menu_client(lang))


@dp.message_handler(text=["Машғулот нархлари", "Цены на обучение"])
async def price(mes: Message):
    r = requests.get(url=f"{BASE_URL}/session/price/list/")
    pr = r.json()
    text = ""
    if lang == 'uz':
        for i in pr:
            text += f"{i['category']} тоифа - {i['price']} сўм соатига\n"
    else:
        for i in pr:
            text += f"{i['category']} категория - {i['price']} в час\n"
    await mes.answer(text)


@dp.message_handler(text=["Профилни ўчириш", "Удалить профиль"])
async def a(mes: Message):
    if lang == 'uz':
        await mes.answer('Профилингизни ўчирмоқчимисиз?', reply_markup=profile_delete(lang))
    else:
        await mes.answer('Хотите удалить свой профиль?', reply_markup=profile_delete(lang))
    await DeleteCl.yes_or_no.set()


@dp.message_handler(state=DeleteCl.yes_or_no)
async def delete_profile(mes: Message, state: FSMContext):
    if (mes.text == 'Ҳа') or (mes.text == 'Да'):
        rp = requests.delete(url=f"{BASE_URL}/client/delete/{mes.from_user.id}/")
        if rp.status_code == 204:
            if lang == 'uz':
                await mes.answer("Профилингиз ўчирилди", reply_markup=ReplyKeyboardRemove())
            else:
                await mes.answer("Ваш профиль был удален", reply_markup=ReplyKeyboardRemove())
        else:
            if lang == 'uz':
                await mes.answer("Нимадир хато кетди қайтадан ўриниб кўринг!")
            else:
                await mes.answer("Попробуйте еще раз, что-то пошло не так!")
    elif (mes.text == 'Йўқ') or (mes.text == 'Нет'):
        if lang == 'uz':
            await mes.answer("Керакли булимни танланг 👇", reply_markup=menu_client(lang))
        else:
            await mes.answer("Выберите нужный раздел 👇", reply_markup=menu_client(lang))
    await state.finish()


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
    if lang == 'uz':
        await call.message.answer(f"{res['message']}", reply_markup=menu_client(lang))
    else:
        await call.message.answer(f"{res['message_ru']}", reply_markup=menu_client(lang))
    await call.answer(cache_time=3)
