from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
import requests
from data.config import BASE_URL
from states.session import SessionForm, SessionEdit
from aiogram.dispatcher import FSMContext
from loader import dp
from keyboards.default.register import stp_btn, str_btn, text_ses
from datetime import datetime, timedelta
from keyboards.inline.calendar import create_calendar, call_data
from keyboards.inline.clock import create_clock
from keyboards.inline.sessions import create_after_sessions_for_ins, before_sessions_for_ins, rate
from utils.notify_admins import notify, notify_session_deleted
from utils.timer import str_obj, stp_obj
from keyboards.default.is_authenticated import menu_client, menu_instructor

lang = ''


@dp.message_handler(text=["Машғулот яратиш", "Создание тренировок"])
async def ax(mes: Message):
    global lang
    if mes.text == 'Машғулот яратиш':
        lang = 'uz'
    elif mes.text == 'Создание тренировок':
        lang = 'ru'
    res = requests.get(url=f"{BASE_URL}/session/")
    cts = res.json()
    if len(cts) == 0:
        if lang == 'uz':
            await mes.answer("Биздан ҳозирча инструcторлар рўйхатдан ўтмаган")
        else:
            await mes.answer("Мы еще не зарегистрировали производителей инструментов")
    else:
        markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
        for i in cts:
            markup.insert(KeyboardButton(text=f"{i['tuman']}"))
        if lang == 'uz':
            await mes.answer('Узингизга қулай бўлган туманни танланг', reply_markup=markup)
        else:
            await mes.answer('Выберите удобный для вас район', reply_markup=markup)
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
    if lang == 'uz':
        await mes.answer(text_ses()['yaratish'], reply_markup=markup)
    else:
        await mes.answer(text_ses()['yaratish_ru'], reply_markup=markup)
    await SessionForm.toifa.set()


@dp.message_handler(state=SessionForm.toifa)
async def get_category(mes: Message, state: FSMContext):
    await state.update_data(
        {'toifa': mes.text}
    )
    cat = await state.get_data()
    res = requests.get(url=f"{BASE_URL}/session/?tum={cat['tuman']}&cat={cat['toifa']}")
    genders = res.json()
    gdr = [i['jins'] for i in genders]
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if lang == 'uz':
        if ('Мужчина' in gdr) or ('Еркак' in gdr):
            markup.insert(KeyboardButton(text=f"Еркак"))
        if ('Женщины' in gdr) or ('Аёл' in gdr):
            markup.insert(KeyboardButton(text=f"Аёл"))
        await mes.answer(text_ses()['jins'], reply_markup=markup)
    else:
        if ('Мужчина' in gdr) or ('Еркак' in gdr):
            markup.insert(KeyboardButton(text=f"Мужчина"))
        if ('Женщины' in gdr) or ('Аёл' in gdr):
            markup.insert(KeyboardButton(text=f"Женщины"))
        await mes.answer(text_ses()['jins_ru'], reply_markup=markup)
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
    if lang == 'uz':
        await mes.answer(text_ses()['moshina'], reply_markup=markup)
    else:
        await mes.answer(text_ses()['moshina_ru'], reply_markup=markup)
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
        markup.insert(KeyboardButton(text=f"{i['ism']} {i['familiya']}\n(Reyting) {star}"))
        loca = i['location']
        lce = loca.split(', ')
        data.append({'ism': i['ism'], 'familiya': i['familiya'], 'card': i['card'], 'ins_tg': i['telegram_id'],
                     'lat': lce[0], 'lon': lce[1]})
    await state.update_data(
        {'ins_data': data, 'moshina': mes.text}
    )
    if lang == 'uz':
        await mes.answer(text_ses()['instructor'], reply_markup=markup)
    else:
        await mes.answer(text_ses()['instructor_ru'], reply_markup=markup)
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
    if lang == 'uz':
        await mes.answer(text_ses()['manzil'])
    else:
        await mes.answer(text_ses()['manzil_ru'])
    ins_data = data['ins_data']
    lat = float(ins_data[0]['lat'])
    lon = float(ins_data[0]['lon'])
    await dp.bot.send_location(latitude=lat, longitude=lon, chat_id=mes.from_user.id)
    if lang == 'uz':
        await mes.answer(text_ses()['kun'], reply_markup=create_calendar())
    else:
        await mes.answer(text_ses()['kun_ru'], reply_markup=create_calendar())
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
            if lang == 'uz':
                await call.message.answer(text_ses()['utgan_kun'], reply_markup=create_calendar())
            else:
                await call.message.answer(text_ses()['utgan_kun_ru'], reply_markup=create_calendar())
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
                if lang == 'uz':
                    await dp.bot.send_message(call.from_user.id,
                                              f"Инструктор мана шу кунга банд қилинган вақтлари бўш вақтини танланг!\n\n{txt}")
                else:
                    await dp.bot.send_message(call.from_user.id,
                                              f"Инструктор в этот день занят, выбирайте его свободное время!\n\n{txt}")
            else:
                await state.update_data(
                    {'free': True}
                )
            await SessionForm.next()
            if lang == 'uz':
                await call.message.answer(text_ses()['vaqt'], reply_markup=create_clock())
            else:
                await call.message.answer(text_ses()['vaqt_ru'], reply_markup=create_clock())
            await call.message.delete()
        await call.answer(cache_time=1)
    elif actions == "PREV-MONTH":
        pre = curr - timedelta(days=1)
        if lang == 'uz':
            await call.message.edit_text("Илтимос кунини танланг!",
                                         reply_markup=create_calendar(int(pre.year), int(pre.month)))
        else:
            await call.message.edit_text("Пожалуйста, выберите день!",
                                         reply_markup=create_calendar(int(pre.year), int(pre.month)))
        await SessionForm.kun.set()
    elif actions == "NEXT-MONTH":
        ne = curr + timedelta(days=31)
        if lang == 'uz':
            await call.message.edit_text("Илтимос кунини танланг!",
                                         reply_markup=create_calendar(int(ne.year), int(ne.month)))
        else:
            await call.message.edit_text("Пожалуйста, выберите день!",
                                         reply_markup=create_calendar(int(ne.year), int(ne.month)))
        await SessionForm.kun.set()
    elif actions == 'IGNORE':
        if lang == 'uz':
            await call.message.answer("Илтимос кунини танланг!",
                                      reply_markup=create_calendar(int(now.year), int(now.month)))
        else:
            await call.message.answer("Пожалуйста, выберите день!",
                                      reply_markup=create_calendar(int(now.year), int(now.month)))
        await call.message.delete()
        await SessionForm.kun.set()
    else:
        if lang == 'uz':
            await call.message.edit_text(text="Бирор нарса нотўғри кетди!",
                                         reply_markup=create_calendar(now.year, now.month))
        else:
            await call.message.edit_text(text="Что-то пошло не так!",
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
                                     reply_markup=create_clock(mn=mn - timedelta(minutes=30), hr=hr))
        await SessionForm.vaqt.set()
    elif actions == "minute⬇️":
        await call.message.edit_text(text="Вақтни танланг:",
                                     reply_markup=create_clock(mn=mn + timedelta(minutes=30), hr=hr))
        await SessionForm.vaqt.set()
    elif actions == "OK":
        data = await state.get_data()
        ins_data = data['ins_data']
        if (ins_data[0]['card'] == 'Ҳа') or (ins_data[0]['card'] == 'Да'):
            if lang == 'uz':
                markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton('Нақд'), KeyboardButton('Карта')]],
                                             resize_keyboard=True)
            else:
                markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton('Наличные'), KeyboardButton('Карта')]],
                                             resize_keyboard=True)
        else:
            if lang == 'uz':
                markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton('Нақд')]],
                                             resize_keyboard=True)
            else:
                markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton('Наличные')]],
                                             resize_keyboard=True)
        dt = data['kun']
        kun = int(dt.split('-')[2])
        if (now.day == kun) and (now.time().hour >= hr.hour) and (now.time().minute > mn.minute):
            if lang == 'uz':
                await call.message.edit_text(text_ses()['utgan_vaqt'], reply_markup=create_clock())
            else:
                await call.message.edit_text(text_ses()['utgan_vaqt_ru'], reply_markup=create_clock())
        else:
            if data['free'] is False:
                r = requests.get(url=f"{BASE_URL}/instructor/free/?tel_id={data['ins_tg_id']}&date={data['kun']}")
                rp = r.json()
                count = len(rp['vaqt'])
                c1 = f"{str(hr)[11:13]}{str(mn)[13:16]}"
                for i in rp['vaqt']:
                    s = datetime.strptime(i, '%H:%M')
                    s1 = s + timedelta(hours=1)
                    s2 = s - timedelta(hours=1)
                    if (datetime.strptime(c1, '%H:%M') >= s1) or (datetime.strptime(c1, '%H:%M') <= s2):
                        count -= 1
                if count:
                    if lang == 'uz':
                        await call.message.answer(text_ses()['band_qilingan_vaqt'], reply_markup=create_clock())
                    else:
                        await call.message.answer(text_ses()['band_qilingan_vaqt_ru'], reply_markup=create_clock())
                    await SessionForm.vaqt.set()
                    await call.message.delete()
                else:
                    await state.update_data(
                        {'soat': f"{hr.hour}:{mn.minute}"}
                    )
                    if lang == 'uz':
                        await call.message.answer(text_ses()['tulov'], reply_markup=markup)
                    else:
                        await call.message.answer(text_ses()['tulov_ru'], reply_markup=markup)
                    await SessionForm.next()
                    await call.message.delete()
            else:
                await state.update_data(
                    {'soat': f"{hr.hour}:{mn.minute}"}
                )
                if lang == 'uz':
                    await call.message.answer(text_ses()['tulov'], reply_markup=markup)
                else:
                    await call.message.answer(text_ses()['tulov_ru'], reply_markup=markup)
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
        if lang == 'uz':
            await mes.answer(text_ses()['mashgulot_yaratilsa'], reply_markup=menu_client(lang))
        else:
            await mes.answer(text_ses()['mashgulot_yaratilsa_ru'], reply_markup=menu_client(lang))
        await notify(instructor=data['ins_tg_id'], lang=lang)
    else:
        if lang == 'uz':
            await mes.answer(text_ses()['mashgulot_yaratilmasa'], reply_markup=menu_client(lang))
        else:
            await mes.answer(text_ses()['mashgulot_yaratilmasa_ru'], reply_markup=menu_client(lang))
    await state.finish()


@dp.callback_query_handler(text=['after', 'before'])
async def get_session(call: CallbackQuery):
    if call.data == 'after':
        r = requests.get(url=f"{BASE_URL}/session/{call.from_user.id}/?page={1}")
        res = r.json()
        row_2 = ""
        for (i, ses) in zip(range(1, 6), res['results']):
            row_2 += f"{i}. {ses['client']} {ses['vaqt']}\n     {ses['c_telefoni']}\n"
        if lang == 'uz':
            await call.message.answer(f"Натижа {res['count']} тa\n" + row_2,
                                      reply_markup=create_after_sessions_for_ins(res, page=1))
        else:
            await call.message.answer(f"Результат {res['count']} раз\n" + row_2,
                                      reply_markup=create_after_sessions_for_ins(res, page=1))
    elif call.data == 'before':
        r = requests.get(url=f"{BASE_URL}/session/finished/{call.from_user.id}/")
        res = r.json()
        row_2 = ""
        for (i, ses) in zip(range(1, 6), res['results']):
            row_2 += f"{i}. {ses['client']} {ses['vaqt']}\n     {ses['c_telefoni']}\n"
        if lang == 'uz':
            await call.message.answer(f"Натижа {res['count']} тa\n" + row_2,
                                      reply_markup=before_sessions_for_ins(page=1))
        else:
            await call.message.answer(f"Результат {res['count']} раз\n" + row_2,
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
        if lang == 'uz':
            await call.message.edit_text(f"Натижа {res['count']} тa\n" + row_2,
                                         reply_markup=create_after_sessions_for_ins(res, page + 1))
        else:
            await call.message.edit_text(f"Результат {res['count']} раз\n" + row_2,
                                         reply_markup=create_after_sessions_for_ins(res, page + 1))
    else:
        if lang == 'uz':
            await call.answer("Бу охирги сахифа!")
        else:
            await call.answer("Это последняя страница!")
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
        if lang == 'uz':
            await call.message.edit_text(f"Натижа {res['count']} тa\n" + row_2,
                                         reply_markup=create_after_sessions_for_ins(res, page - 1))
        else:
            await call.message.edit_text(f"Результат {res['count']} раз\n" + row_2,
                                         reply_markup=create_after_sessions_for_ins(res, page - 1))
    else:
        if lang == 'uz':
            await call.answer("Бу биринчи сахифа!")
        else:
            await call.answer("Это первая страница!")
    await call.answer(cache_time=3)


@dp.callback_query_handler(text_contains='id:')
async def a(call: CallbackQuery, state: FSMContext):
    s_id = call.data.split('id:')[1]
    await state.update_data({'session_id': s_id})
    if lang == 'uz':
        await call.message.answer("Керакли булимни танланг 👇", reply_markup=str_btn(lang))
    else:
        await call.message.answer("Выберите нужный раздел 👇", reply_markup=str_btn(lang))
    await call.answer(cache_time=1)
    await SessionEdit.start.set()


@dp.message_handler(state=SessionEdit.start)
async def get_ses(mes: Message, state: FSMContext):
    if (mes.text == 'Машғулотни бекор килиш') or (mes.text == 'Отменить тренировку'):
        data = await state.get_data()
        rp = requests.delete(url=f"{BASE_URL}/session/detail/{data['session_id']}/")
        rs = rp.json()
        if rp.status_code == 200:
            if lang == 'uz':
                await mes.answer("Машғулот ўчирилди", reply_markup=menu_instructor(lang))
            else:
                await mes.answer("Тренировка удалена", reply_markup=menu_instructor(lang))
            await notify_session_deleted(instructor=rs['id2'], time=rs['vaqt'], lang=lang)
        await state.finish()
    elif (mes.text == 'Бошлаш') or (mes.text == 'Начать'):
        str_obj()
        if lang == 'uz':
            await mes.answer("Вақт кетди\nТугатиш тугмасини босиш эсингиздан чиқмасин!!!", reply_markup=stp_btn(lang))
        else:
            await mes.answer("Время ушло\nНе забудьте нажать кнопку Завершить!!!", reply_markup=stp_btn(lang))
        await SessionEdit.next()
    elif (mes.text == '⬅️Oртга') or (mes.text == '⬅️Назад'):
        if lang == 'uz':
            await mes.answer("Керакли бўлимни танланг 👇", reply_markup=menu_instructor(lang))
        else:
            await mes.answer("Выберите нужный раздел 👇", reply_markup=menu_instructor(lang))
        await state.finish()


@dp.message_handler(text=['Тугатиш', "Завершить"], state=SessionEdit.finish)
async def finish(mes: Message, state: FSMContext):
    s_id = await state.get_data()
    r = requests.get(url=f"{BASE_URL}/session/price/?s_id={s_id['session_id']}")
    res = r.json()
    price = round((res['price'] / 60) / 100) * 100
    minute = stp_obj()
    if minute > 120:
        minute = 120
        if lang == 'uz':
            await mes.answer("Тугатишни босиш есингиздан чиқиб кетди вақтни 2 соат бўлганида тугатдим!!!")
        else:
            await mes.answer("Нажав кнопку Готово, вы не в своем уме, я закончил время, когда было 2 часа!!!")
    summa = minute * price
    # if res['qayerdan'] == 'Уйдан':
    #     summa += 15000
    rp = requests.patch(url=f"{BASE_URL}/session/detail/{s_id['session_id']}/?ins={mes.from_user.id}",
                        data={'summa': summa})
    rs = rp.json()
    if lang == 'uz':
        # await mes.answer(f"{summa} сўм бўлди\nСизнинг балансенингиз {rs['balance']} сўм", reply_markup=menu_instructor)
        await mes.answer(f"{summa} сўм бўлди", reply_markup=menu_instructor(lang))
        await dp.bot.send_message(rs['client'],
                                  f"{summa} сўм бўлди\nИнстркторга 1 дан 5 гача бўлган қийматда баҳоланг!",
                                  reply_markup=rate)
    else:
        # await mes.answer(f"{summa} сўм бўлди\nСизнинг балансенингиз {rs['balance']} сўм", reply_markup=menu_instructor)
        await mes.answer(f"{summa} сум стал", reply_markup=menu_instructor(lang))
        await dp.bot.send_message(rs['client'],
                                  f"Стоимость занятие {summa} сум\nОцените прибор по значению от 1 до 5!",
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
        if lang == 'uz':
            await call.message.edit_text(f"Натижа {res['count']} та\n" + row_2,
                                         reply_markup=before_sessions_for_ins(page + 1))
        else:
            await call.message.edit_text(f"Результат {res['count']} раз\n" + row_2,
                                         reply_markup=before_sessions_for_ins(page + 1))
    else:
        if lang == 'uz':
            await call.answer("Бу охирги сахифа!")
        else:
            await call.answer("Это последняя страница!")
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
        if lang == 'uz':
            await call.message.edit_text(f"Натижа {res['count']} та\n" + row_2,
                                         reply_markup=before_sessions_for_ins(page - 1))
        else:
            await call.message.edit_text(f"Результат {res['count']} раз\n" + row_2,
                                         reply_markup=before_sessions_for_ins(page - 1))
    else:
        if lang == 'uz':
            await call.answer("Бу биринчи сахифа!")
        else:
            await call.answer("Это первая страница!")
    await call.answer(cache_time=3)
