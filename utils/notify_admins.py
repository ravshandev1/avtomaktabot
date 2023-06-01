import logging
from data.config import ADMINS
from loader import dp


async def on_startup_notify():
    if ADMINS:
        for admin in ADMINS:
            try:
                await dp.bot.send_message(admin, "Бот ишга тушди!!!")

            except Exception as err:
                logging.exception(err)
    pass


async def notify(instructor: int, lang: str):
    if lang == 'uz':
        await dp.bot.send_message(instructor, "Сизга янги машғулот банд қилинди")
    else:
        await dp.bot.send_message(instructor, "Вы заняты новым тренингом")


async def notify_session_deleted(instructor: int, time: str, lang: str):
    if lang == 'uz':
        await dp.bot.send_message(instructor, f"{time} мана шу кундаги машғулот бекор қилинди!")
    else:
        await dp.bot.send_message(instructor, f"{time} именно здесь тренировка в этот день была отменена!")
