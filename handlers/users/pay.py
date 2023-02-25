from aiogram.types import Message, PreCheckoutQuery, LabeledPrice, ReplyKeyboardRemove
from states.instructor import Balans
from aiogram.dispatcher import FSMContext
from data.config import PROVIDER_TOKEN, BASE_URL
from loader import bot, dp
from keyboards.default.is_authenticated import menu_instructor
import requests


@dp.message_handler(text="Балансни тўлдириш")
async def get_summa(mes: Message):
    await mes.answer("Балансингизни тулдтрмокчи булган суммани критинг:", reply_markup=ReplyKeyboardRemove())
    await Balans.summa.set()


@dp.message_handler(state=Balans.summa)
async def balans(mes: Message, state: FSMContext):
    await state.update_data(
        {'summa': int(mes.text) * 100}
    )
    summa = LabeledPrice(label='balansingiz uchun to\'lov', amount=int(mes.text) * 100)
    await bot.send_invoice(
        mes.chat.id,
        title='Balansni to\'ldirish',
        description='Балансингиз учун тўловни амалга оширинг',
        payload='some-invoice',
        provider_token=PROVIDER_TOKEN,
        currency='UZS',
        prices=[summa],
        photo_url='https://www.google.com/url?sa=i&url=https%3A%2F%2Fstock.adobe.com%2Fsearch%2Fimages%3Fk%3Dintention&psig=AOvVaw3QKMdmFOkNVIM6O5Y8y3Cp&ust=1677329570718000&source=images&cd=vfe&ved=0CBAQjRxqFwoTCMiJ6eaZrv0CFQAAAAAdAAAAABAE',
        photo_width=1000,
        photo_height=667,
        provider_data={}
    )
    await state.finish()


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)
    summa = pre_checkout_q.total_amount
    requests.post(url=f"{BASE_URL}/instructor/balanse/",
                  data={'summa': summa, 'instructor': pre_checkout_q.from_user.id})
    await bot.send_message(chat_id=pre_checkout_q.from_user.id, text="Tулов амалга оширилди!",
                           reply_markup=menu_instructor)
