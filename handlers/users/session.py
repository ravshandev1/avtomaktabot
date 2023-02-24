from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
import requests
from data.config import BASE_URL
from states.session import SessionForm, SessionEdit
from aiogram.dispatcher import FSMContext
from loader import dp
from keyboards.default.register import where, payment, stp_btn, str_btn
from datetime import datetime, timedelta
from keyboards.inline.calendar import create_calendar, call_data
from keyboards.inline.clock import create_clock
from keyboards.inline.sessions import create_after_sessions_for_ins, before_sessions_for_ins, rate
from utils.notify_admins import notify
from utils.timer import str_obj, stp_obj
from keyboards.default.is_authenticated import menu_client, menu_instructor


@dp.message_handler(text='Session yaratish')
async def session(mes: Message):
    res = requests.get(url=f"{BASE_URL}/session/")
    cts = res.json()
    if len(cts) == 0:
        await mes.answer("Bizdan hozircha instructorlar ro'yxatdan o'tmagan")
    else:
        markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
        for i in cts:
            markup.insert(KeyboardButton(text=f"{i['toifa']}"))
        await mes.answer('Bizda mavjud toifalar\nQaysi toifani o\'rganmoqchisiz!', reply_markup=markup)
        await SessionForm.toifa.set()


@dp.message_handler(state=SessionForm.toifa)
async def get_category(mes: Message, state: FSMContext):
    await state.update_data(
        {'toifa': mes.text}
    )
    cat = await state.get_data()
    res = requests.get(url=f"{BASE_URL}/session/?cat={cat['toifa']}")
    genders = res.json()
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for i in genders:
        markup.insert(KeyboardButton(text=f"{i['jins']}"))
    await mes.answer('Instruktir jinsini tanlang', reply_markup=markup)
    await SessionForm.next()


@dp.message_handler(state=SessionForm.jins)
async def get_gender(mes: Message, state: FSMContext):
    await state.update_data(
        {'jins': mes.text}
    )
    gen = await state.get_data()
    res = requests.get(url=f"{BASE_URL}/session/?cat={gen['toifa']}&gen={gen['jins']}")
    cars = res.json()
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    for i in cars:
        markup.insert(KeyboardButton(text=f"{i['moshina']}"))
    await mes.answer('Qanaqa moshinada o\'rganmoqchisiz', reply_markup=markup)
    await SessionForm.next()


@dp.message_handler(state=SessionForm.moshina)
async def get_car(mes: Message, state: FSMContext):
    await state.update_data(
        {'moshina': mes.text}
    )
    car = await state.get_data()
    res = requests.get(url=f"{BASE_URL}/session/?cat={car['toifa']}&gen={car['jins']}&car={car['moshina']}")
    ins = res.json()
    data = list()
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    for i in ins:
        markup.insert(KeyboardButton(text=f"{i['ism']}"))
        data.append({'ins_ism': i['ism'], 'ins_tg': i['telegram_id']})
    await state.update_data(
        {'ins_data': data}
    )
    await mes.answer("Instruktirni tanlang", reply_markup=markup)
    await SessionForm.next()


@dp.message_handler(state=SessionForm.instructor)
async def get_instructor(mes: Message, state: FSMContext):
    data = await state.get_data()
    tg = None
    for i in data['ins_data']:
        if i['ins_ism'] == mes.text:
            tg = i['ins_tg']
    await state.update_data(
        {'instructor': mes.text, 'ins_tg_id': tg}
    )
    await mes.answer("Instruktir sizni qayerdan olib ketsin?", reply_markup=where)
    await SessionForm.next()


@dp.message_handler(state=SessionForm.qayerdan)
async def get_location(mes: Message, state: FSMContext):
    await state.update_data(
        {'qayerdan': mes.text}
    )
    markup = create_calendar()
    await mes.answer("Kunni tanlang", reply_markup=markup)
    await SessionForm.next()


@dp.callback_query_handler(state=SessionForm.kun)
async def get_day(call: CallbackQuery, state: FSMContext):
    now = datetime.now()
    a = call_data(call.data)
    actions, year, month, day = a
    curr = datetime(int(year), int(month), 1)
    if actions == "DAY":
        ret_data = datetime(int(year), int(month), int(day))
        await state.update_data(
            {'kun': f"{year}-{month}-{day}"}
        )
        if (now.year >= ret_data.year) and (now.month >= ret_data.month) and (now.day > ret_data.day):
            await call.message.answer("O'tib ketgan kunni tanlab bulmaydi!\nIltimos endi keladigan kunni tanlang!",
                                      reply_markup=create_calendar())
            await call.message.delete()
        else:
            await SessionForm.next()
            await call.message.answer(text='Vaqtni tanlang:', reply_markup=create_clock())
            await call.message.delete()
        await call.answer(cache_time=1)
    elif actions == "PREV-MONTH":
        pre = curr - timedelta(days=1)
        await call.message.edit_text("Iltimos kunini tanlang!",
                                     reply_markup=create_calendar(int(pre.year), int(pre.month)))
        await SessionForm.kun.set()
    elif actions == "NEXT-MONTH":
        ne = curr + timedelta(days=31)
        await call.message.edit_text("Iltimos vajdeniya kunini tanlang!",
                                     reply_markup=create_calendar(int(ne.year), int(ne.month)))
        await SessionForm.kun.set()
    elif actions == 'IGNORE':
        await call.message.answer("Iltimos kunini tanlang!",
                                  reply_markup=create_calendar(int(now.year), int(now.month)))
        await call.message.delete()
        await SessionForm.kun.set()
    else:
        await call.message.edit_text(text="Biror narsa noto'g'ri ketdi!",
                                     reply_markup=create_calendar(now.year, now.month))
        await SessionForm.kun.set()


@dp.callback_query_handler(state=SessionForm.vaqt)
async def get_date(call: CallbackQuery, state: FSMContext):
    now = datetime.now()
    a = call_data(call.data)
    actions, hr, mn = a
    hr = datetime.strptime(hr, "%H")
    mn = datetime.strptime(mn, "%M")
    if actions == "hour⬆️":
        await call.message.edit_text(text="Vaqtni tanlang:",
                                     reply_markup=create_clock(hr=hr - timedelta(hours=1), mn=mn))
        await SessionForm.vaqt.set()
    elif actions == "hour⬇️":
        await call.message.edit_text(text="Vaqtni tanlang:",
                                     reply_markup=create_clock(hr=hr + timedelta(hours=1), mn=mn))
        await SessionForm.vaqt.set()
    elif actions == "minute⬆️":
        await call.message.edit_text(text="Vaqtni tanlang:",
                                     reply_markup=create_clock(mn=mn - timedelta(minutes=1), hr=hr))
        await SessionForm.vaqt.set()
    elif actions == "minute⬇️":
        await call.message.edit_text(text="Vaqtni tanlang:",
                                     reply_markup=create_clock(mn=mn + timedelta(minutes=1), hr=hr))
        await SessionForm.vaqt.set()
    elif actions == "OK":
        data = await state.get_data()
        dt = data['kun']
        kun = int(dt.split('-')[2])
        if (now.day == kun) and (now.time().hour >= hr.hour) and (now.time().minute > mn.minute):
            await call.message.edit_text(text="O'tib ketgan vaqtni tanlab bo'lmaydi\nIltimos vaqtni tanlang:",
                                         reply_markup=create_clock())
        else:
            await state.update_data(
                {'soat': f"{hr.hour}:{mn.minute}:00+05:00"}
            )
            await call.message.answer(text='Tulov turini tanlang:', reply_markup=payment)
            await SessionForm.next()
            await call.message.delete()
    await call.answer(cache_time=1)


@dp.message_handler(state=SessionForm.tulov_turi)
async def get_payent_method(mes: Message, state: FSMContext):
    await state.update_data(
        {'tulov_turi': mes.text, 'telegram_id': mes.from_user.id}
    )
    data = await state.get_data()
    data['vaqt'] = f"{data['kun']} {data['soat']}"
    del data['soat']
    del data['kun']
    rp = requests.post(url=f"{BASE_URL}/session/", data=data)
    await notify(data['ins_tg_id'])
    if rp.status_code == 200:
        await mes.answer("Sessiya muvaffaqiyatli yaratildi!", reply_markup=menu_client)
    else:
        await mes.answer("Xato ketdi qaytadan o'rinib ko'ring!")
    await state.finish()


@dp.callback_query_handler(text=['after', 'before'])
async def get_session(call: CallbackQuery):
    if call.data == 'after':
        r = requests.get(url=f"{BASE_URL}/session/{call.from_user.id}/?page={1}")
        res = r.json()
        row_2 = ""
        for (i, ses) in zip(range(1, 6), res['results']):
            row_2 += f"{i}.{ses['client']} {ses['qayerdan']} {ses['vaqt']}\n     {ses['c_telefoni']}\n"
        await call.message.answer(f"Natija {res['count']} ta\n" + row_2,
                                  reply_markup=create_after_sessions_for_ins(res, page=1))
    elif call.data == 'before':
        r = requests.get(url=f"{BASE_URL}/session/finished/{call.from_user.id}/")
        res = r.json()
        row_2 = ""
        for (i, ses) in zip(range(1, 6), res['results']):
            row_2 += f"{i}.{ses['client']} {ses['qayerdan']} {ses['vaqt']}\n     {ses['c_telefoni']}\n"
        await call.message.answer(f"Natija {res['count']} ta\n" + row_2,
                                  reply_markup=before_sessions_for_ins(page=1))
    await call.answer(cache_time=3)


@dp.callback_query_handler(text_contains='next')
async def action(call: CallbackQuery):
    page = int(call.data.split('next:')[1])
    r = requests.get(url=f"{BASE_URL}/session/{call.from_user.id}/?page={page}")
    res = r.json()
    if res['next']:
        r1 = requests.get(url=f"{BASE_URL}/session/{call.from_user.id}/?page={page + 1}")
        res = r1.json()
        row_2 = ""
        for (i, ses) in zip(range(1, 6), res['results']):
            row_2 += f"{i}.{ses['client']} {ses['qayerdan']} {ses['vaqt']}\n     {ses['c_telefoni']}\n"
        await call.message.edit_text(f"Natija {res['count']} ta\n" + row_2,
                                     reply_markup=create_after_sessions_for_ins(res, page + 1))
    else:
        await call.answer("Bu oxirgi saxifa!")
    await call.answer(cache_time=3)


@dp.callback_query_handler(text_contains='previous')
async def action(call: CallbackQuery):
    page = int(call.data.split('previous:')[1])
    r = requests.get(url=f"{BASE_URL}/session/{call.from_user.id}/?page={page}")
    res = r.json()
    if res['previous']:
        r1 = requests.get(url=f"{BASE_URL}/session/{call.from_user.id}/?page={page - 1}")
        res = r1.json()
        row_2 = ""
        for (i, ses) in zip(range(1, 6), res['results']):
            row_2 += f"{i}.{ses['client']} {ses['qayerdan']} {ses['vaqt']}\n     {ses['c_telefoni']}\n"
        await call.message.edit_text(f"Natija {res['count']} ta\n" + row_2,
                                     reply_markup=create_after_sessions_for_ins(res, page - 1))
    else:
        await call.answer("Bu birinchi saxifa!")
    await call.answer(cache_time=3)


@dp.callback_query_handler(text_contains='id:')
async def get_ses(call: CallbackQuery, state: FSMContext):
    s_id = call.data.split('id:')[1]
    rp = requests.get(url=f"{BASE_URL}/instructor/{call.from_user.id}/")
    res = rp.json()
    if res['balans'] > 15000:
        await state.update_data(
            {'session_id': s_id}
        )
        await call.message.answer("Boshlashni bosing 👇", reply_markup=str_btn)
        await call.answer(cache_time=3)
        await SessionEdit.start.set()
    else:
        await call.message.answer("Balansingiz 15 000 so'mdan kam\nIltimos balansingizni to'ldiring!!!")


@dp.message_handler(text='Boshlash', state=SessionEdit.start)
async def start(mes: Message):
    str_obj()
    await mes.answer("Vaqt ketdi\nTugatishni to'gmasini bosish esingizdan chiqmasin!!!", reply_markup=stp_btn)
    await SessionEdit.next()


@dp.message_handler(text='Tugatish', state=SessionEdit.finish)
async def finish(mes: Message, state: FSMContext):
    s_id = await state.get_data()
    r = requests.get(url=f"{BASE_URL}/session/price/")
    res = r.json()
    price = round((res[0]['price'] / 60) / 100) * 100
    minute = stp_obj()
    if minute > 120:
        minute = 120
        await mes.answer("Tugatishni bosish esingizdan chiqib ketdi vaqtni 2 soat bo'lganida tugatdim!!!")
    summa = minute * price
    rp = requests.patch(url=f"{BASE_URL}/session/detail/{s_id['session_id']}/?ins={mes.from_user.id}",
                        data={'summa': summa})
    rs = rp.json()
    await mes.answer(f"{summa} so'm buldi\nSizning balanseningiz {rs['balance']} so'm", reply_markup=menu_instructor)
    await dp.bot.send_message(rs['client'], "Instructorga 1 dan 5 gacha bo'lgan qiymatda baholang!",
                              reply_markup=rate)
    requests.post(url=f"{BASE_URL}/instructor/rating/", data={'instructor': mes.from_user.id, 'client': rs['client']})
    await state.finish()


@dp.callback_query_handler(text_contains='keyingi')
async def action(call: CallbackQuery):
    page = int(call.data.split('keyingi:')[1])
    r = requests.get(url=f"{BASE_URL}/session/finished/{call.from_user.id}/?page={page}")
    res = r.json()
    if res['next']:
        r1 = requests.get(url=f"{BASE_URL}/session/finished/{call.from_user.id}/?page={page + 1}")
        res = r1.json()
        row_2 = ""
        for (i, ses) in zip(range(1, 6), res['results']):
            row_2 += f"{i}.{ses['client']} {ses['qayerdan']} {ses['vaqt']}\n     {ses['c_telefoni']}\n"
        await call.message.edit_text(f"Natija {res['count']} ta\n" + row_2,
                                     reply_markup=before_sessions_for_ins(page + 1))
    else:
        await call.answer("Bu oxirgi saxifa!")
    await call.answer(cache_time=3)


@dp.callback_query_handler(text_contains='oldingi')
async def action(call: CallbackQuery):
    page = int(call.data.split('oldingi:')[1])
    r = requests.get(url=f"{BASE_URL}/session/finished/{call.from_user.id}/?page={page}")
    res = r.json()
    if res['previous']:
        r1 = requests.get(url=f"{BASE_URL}/session/finished/{call.from_user.id}/?page={page - 1}")
        res = r1.json()
        row_2 = ""
        for (i, ses) in zip(range(1, 6), res['results']):
            row_2 += f"{i}.{ses['client']} {ses['qayerdan']} {ses['vaqt']}\n     {ses['c_telefoni']}\n"
        await call.message.edit_text(f"Natija {res['count']} ta\n" + row_2,
                                     reply_markup=before_sessions_for_ins(page - 1))
    else:
        await call.answer("Bu birinchi saxifa!")
    await call.answer(cache_time=3)
