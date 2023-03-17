from aiogram import types
from loader import dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandHelp


@dp.message_handler(CommandHelp(), state='*')
async def bot_help(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Бот қайта ишга тушурилди!\n/start ни босинг!')
