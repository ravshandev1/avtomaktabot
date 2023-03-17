from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
import requests
from data.config import BASE_URL
from states.session import SessionForm, SessionEdit
from aiogram.dispatcher import FSMContext
from loader import dp
from keyboards.default.register import stp_btn, str_btn, regions
from datetime import datetime, timedelta
from keyboards.inline.calendar import create_calendar, call_data
from keyboards.inline.clock import create_clock
from keyboards.inline.sessions import create_after_sessions_for_ins, before_sessions_for_ins, rate
from utils.notify_admins import notify
from utils.timer import str_obj, stp_obj
from keyboards.default.is_authenticated import menu_client, menu_instructor


@dp.message_handler(text="Машғулот яратиш")
async def ax(mes: Message):
    res = requests.get(url=f"{BASE_URL}/session/")
    cts = res.json()
    if len(cts) == 0:
        await mes.answer("Биздан ҳозирча инструcторлар рўйхатдан ўтмаган")
    else:
        markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
        for i in cts:
            markup.insert(KeyboardButton(text=f"{i['tuman']}"))
        await mes.answer('Узингизга қулай бўлган туманни танланг', reply_markup=markup)
        await SessionForm.tuman.set()


@dp.message_handler(state=SessionForm.tuman)
async def session(mes: Message, state: FSMContext):
    res = requests.get(url=f"{BASE_URL}/session/?tum={mes.text}")
    cts = res.json()
    await state.update_data(
        {'tuman': mes.text}
    )
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    for i in cts:
        markup.insert(KeyboardButton(text=f"{i['toifa_name']}"))
    await mes.answer('Бизда мавжуд тоифалар\nҚайси тоифани ўрганмоқчисиз!', reply_markup=markup)
    await SessionForm.toifa.set()


@dp.message_handler(state=SessionForm.toifa)
async def get_category(mes: Message, state: FSMContext):
    await state.update_data(
        {'toifa': mes.text}
    )
    cat = await state.get_data()
    res = requests.get(url=f"{BASE_URL}/session/?tum={cat['tuman']}&cat={cat['toifa']}")
    genders = res.json()
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for i in genders:
        markup.insert(KeyboardButton(text=f"{i['jins']}"))
    await mes.answer('Инструктир жинсини танланг', reply_markup=markup)
    await SessionForm.next()


@dp.message_handler(state=SessionForm.jins)
async def get_gender(mes: Message, state: FSMContext):
    await state.update_data(
        {'jins': mes.text}
    )
    gen = await state.get_data()
    res = requests.get(url=f"{BASE_URL}/session/?tum={gen['tuman']}&cat={gen['toifa']}&gen={gen['jins']}")
    cars = res.json()
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    for i in cars:
        markup.insert(KeyboardButton(text=f"{i['moshina']}"))
    await mes.answer('Қанақа мошинада ўрганмоқчисиз', reply_markup=markup)
    await SessionForm.next()


@dp.message_handler(state=SessionForm.moshina)
async def get_car(mes: Message, state: FSMContext):
    car = await state.get_data()
    res = requests.get(
        url=f"{BASE_URL}/session/?tum={car['tuman']}&cat={car['toifa']}&gen={car['jins']}&car={mes.text}")
    ins = res.json()
    data = list()
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    for i in ins:
        star = ""
        for j in range(i['get_rating']):
            star += "⭐️"
        markup.insert(KeyboardButton(text=f"{i['ism']} {i['familiya']}\n{star}"))
        loca = i['location']
        lce = loca.split(', ')
        data.append({'ism': i['ism'], 'familiya': i['familiya'], 'card': i['card'], 'ins_tg': i['telegram_id'],
                     'lat': lce[0], 'lon': lce[1]})
    await state.update_data(
        {'ins_data': data, 'moshina': mes.text}
    )
    await mes.answer("Инструктирни танланг", reply_markup=markup)
    await SessionForm.next()


@dp.message_handler(state=SessionForm.instructor)
async def get_instructor(mes: Message, state: FSMContext):
    data = await state.get_data()
    tg = None
    for i in data['ins_data']:
        ls = mes.text.split()
        if (i['ism'] == ls[0]) and (i['familiya'] == ls[1]):
            tg = i['ins_tg']
    await state.update_data(
        {'instructor': mes.text, 'ins_tg_id': tg}
    )
    await mes.answer("Машғулот бўладиган манзил")
    ins_data = data['ins_data']
    lat = float(ins_data[0]['lat'])
    lon = float(ins_data[0]['lon'])
    await dp.bot.send_location(latitude=lat, longitude=lon, chat_id=mes.from_user.id)
    await mes.answer("Машғулот кунини танланг", reply_markup=create_calendar())
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
        dat = await state.get_data()
        if (now.year >= ret_data.year) and (now.month >= ret_data.month) and (now.day > ret_data.day):
            await call.message.answer("Ўтиб кетган кунни танлаб булмайди!\nИлтимос енди келадиган кунни танланг!",
                                      reply_markup=create_calendar())
            await call.message.delete()
        else:
            r = requests.get(url=f"{BASE_URL}/instructor/free/?tel_id={dat['ins_tg_id']}&date={dat['kun']}")
            rp = r.json()
            if rp['vaqt'] != 'Band qilinmagan!':
                await state.update_data(
                    {'free': False}
                )
                txt = ""
                for i in rp['vaqt']:
                    txt += f"{i}\n"
                await dp.bot.send_message(call.from_user.id,
                                          f"Инструкторни мана шу кунга банд қилинган вақтлари инструкторни банд бўлмаган вақтини танланг!\n\n{txt}")
            else:
                await state.update_data(
                    {'free': True}
                )
            await SessionForm.next()
            await call.message.answer(text='Вақтни танланг:', reply_markup=create_clock())
            await call.message.delete()
        await call.answer(cache_time=1)
    elif actions == "PREV-MONTH":
        pre = curr - timedelta(days=1)
        await call.message.edit_text("Илтимос кунини танланг!",
                                     reply_markup=create_calendar(int(pre.year), int(pre.month)))
        await SessionForm.kun.set()
    elif actions == "NEXT-MONTH":
        ne = curr + timedelta(days=31)
        await call.message.edit_text("Илтимос кунини танланг!",
                                     reply_markup=create_calendar(int(ne.year), int(ne.month)))
        await SessionForm.kun.set()
    elif actions == 'IGNORE':
        await call.message.answer("Илтимос кунини танланг!",
                                  reply_markup=create_calendar(int(now.year), int(now.month)))
        await call.message.delete()
        await SessionForm.kun.set()
    else:
        await call.message.edit_text(text="Бирор нарса нотўғри кетди!",
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
        await call.message.edit_text(text="Вақтни танланг:",
                                     reply_markup=create_clock(hr=hr - timedelta(hours=1), mn=mn))
        await SessionForm.vaqt.set()
    elif actions == "hour⬇️":
        await call.message.edit_text(text="Вақтни танланг:",
                                     reply_markup=create_clock(hr=hr + timedelta(hours=1), mn=mn))
        await SessionForm.vaqt.set()
    elif actions == "minute⬆️":
        await call.message.edit_text(text="Вақтни танланг:",
                                     reply_markup=create_clock(mn=mn - timedelta(minutes=1), hr=hr))
        await SessionForm.vaqt.set()
    elif actions == "minute⬇️":
        await call.message.edit_text(text="Вақтни танланг:",
                                     reply_markup=create_clock(mn=mn + timedelta(minutes=1), hr=hr))
        await SessionForm.vaqt.set()
    elif actions == "OK":
        data = await state.get_data()
        ins_data = data['ins_data']
        if ins_data[0]['card'] == 'Ҳа':
            markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton('Нақд'), KeyboardButton('Карта')]],
                                         resize_keyboard=True)
        else:
            markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton('Нақд')]],
                                         resize_keyboard=True)
        dt = data['kun']
        kun = int(dt.split('-')[2])
        if (now.day == kun) and (now.time().hour >= hr.hour) and (now.time().minute > mn.minute):
            await call.message.edit_text(text="Ўтиб кетган вақтни танлаб бўлмайди\nИлтимос вақтни танланг:",
                                         reply_markup=create_clock())
        else:
            if data['free'] is False:
                r = requests.get(url=f"{BASE_URL}/instructor/free/?tel_id={data['ins_tg_id']}&date={data['kun']}")
                rp = r.json()
                vq_1 = list()
                vq_2 = list()
                for i in rp['vaqt']:
                    i = int(i[:2])
                    v1 = i + 1
                    v2 = i - 1
                    vq_1.append(str(v1))
                    vq_2.append(str(v2))
                if (f"{str(hr)[11:13]}" in vq_1) or (f"{str(hr)[11:13]}" in vq_2):
                    await call.message.answer(
                        text="Танлаган вақтиз банд қилинган вақтлардан 1 соат фарқ қилсин!",
                        reply_markup=create_clock())
                    await SessionForm.vaqt.set()
                    await call.message.delete()
                else:
                    await state.update_data(
                        {'soat': f"{hr.hour}:{mn.minute}"}
                    )

                    await call.message.answer(text='Тулов турини танланг:', reply_markup=markup)
                    await SessionForm.next()
                    await call.message.delete()
            else:
                await state.update_data(
                    {'soat': f"{hr.hour}:{mn.minute}"}
                )
                await call.message.answer(text='Тулов турини танланг:', reply_markup=markup)
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
    rp = requests.post(url=f"{BASE_URL}/session/", data=data)
    if rp.status_code == 200:
        await mes.answer("Машғулот муваффақиятли яратилди!", reply_markup=menu_client)
        await notify(data['ins_tg_id'])
    else:
        await mes.answer("Хато кетди қайтадан ўриниб кўринг!", reply_markup=menu_client)
    await state.finish()


@dp.callback_query_handler(text=['after', 'before'])
async def get_session(call: CallbackQuery):
    if call.data == 'after':
        r = requests.get(url=f"{BASE_URL}/session/{call.from_user.id}/?page={1}")
        res = r.json()
        row_2 = ""
        for (i, ses) in zip(range(1, 6), res['results']):
            row_2 += f"{i}. {ses['client']} {ses['vaqt']}\n     {ses['c_telefoni']}\n"
        await call.message.answer(f"Натижа {res['count']} тa\n" + row_2,
                                  reply_markup=create_after_sessions_for_ins(res, page=1))
    elif call.data == 'before':
        r = requests.get(url=f"{BASE_URL}/session/finished/{call.from_user.id}/")
        res = r.json()
        row_2 = ""
        for (i, ses) in zip(range(1, 6), res['results']):
            row_2 += f"{i}. {ses['client']} {ses['vaqt']}\n     {ses['c_telefoni']}\n"
        await call.message.answer(f"Натижа {res['count']} тa\n" + row_2,
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
            row_2 += f"{i}. {ses['client']} {ses['qayerdan']} {ses['vaqt']}\n     {ses['c_telefoni']}\n"
        await call.message.edit_text(f"Натижа {res['count']} тa\n" + row_2,
                                     reply_markup=create_after_sessions_for_ins(res, page + 1))
    else:
        await call.answer("Бу охирги сахифа!")
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
            row_2 += f"{i}. {ses['client']} {ses['qayerdan']} {ses['vaqt']}\n     {ses['c_telefoni']}\n"
        await call.message.edit_text(f"Натижа {res['count']} тa\n" + row_2,
                                     reply_markup=create_after_sessions_for_ins(res, page - 1))
    else:
        await call.answer("Бу биринчи сахифа!")
    await call.answer(cache_time=3)


@dp.callback_query_handler(text_contains='id:')
async def get_ses(call: CallbackQuery, state: FSMContext):
    s_id = call.data.split('id:')[1]
    # rp = requests.get(url=f"{BASE_URL}/instructor/{call.from_user.id}/")
    # res = rp.json()
    # if res['balans'] > 15000:
    await state.update_data({'session_id': s_id})
    await call.message.answer("Бошлашни босинг 👇", reply_markup=str_btn)
    await call.answer(cache_time=3)
    await SessionEdit.start.set()
    # else:
    # await call.message.answer("Бошлашни босинг 👇", reply_markup=str_btn)
    # await call.answer(cache_time=3)


@dp.message_handler(text='Бошлаш', state=SessionEdit.start)
async def start(mes: Message):
    str_obj()
    await mes.answer("Вақт кетди\nТўгатиш тўгмасини босиш есингиздан чиқмасин!!!", reply_markup=stp_btn)
    await SessionEdit.next()


@dp.message_handler(text='Тугатиш', state=SessionEdit.finish)
async def finish(mes: Message, state: FSMContext):
    s_id = await state.get_data()
    r = requests.get(url=f"{BASE_URL}/session/price/?s_id={s_id['session_id']}")
    res = r.json()
    price = round((res['price'] / 60) / 100) * 100
    minute = stp_obj()
    if minute > 120:
        minute = 120
        await mes.answer("Тугатишни босиш есингиздан чиқиб кетди вақтни 2 соат бўлганида тугатдим!!!")
    summa = minute * price
    # if res['qayerdan'] == 'Уйдан':
    #     summa += 15000
    rp = requests.patch(url=f"{BASE_URL}/session/detail/{s_id['session_id']}/?ins={mes.from_user.id}",
                        data={'summa': summa})
    rs = rp.json()
    # await mes.answer(f"{summa} сўм бўлди\nСизнинг балансенингиз {rs['balance']} сўм", reply_markup=menu_instructor)
    await mes.answer(f"{summa} сўм бўлди", reply_markup=menu_instructor)
    await dp.bot.send_message(rs['client'], f"{summa} сўм бўлди\nИнстркторга 1 дан 5 гача бўлган қийматда баҳоланг!",
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
        await call.message.edit_text(f"Натижа {res['count']} та\n" + row_2,
                                     reply_markup=before_sessions_for_ins(page + 1))
    else:
        await call.answer("Бу охирги сахифа!")
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
        await call.message.edit_text(f"Натижа {res['count']} та\n" + row_2,
                                     reply_markup=before_sessions_for_ins(page - 1))
    else:
        await call.answer("Бу биринчи сахифа!")
    await call.answer(cache_time=3)
