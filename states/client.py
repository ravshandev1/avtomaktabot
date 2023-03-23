from aiogram.dispatcher.filters.state import State, StatesGroup


class ClientForm(StatesGroup):
    ism = State()
    familiya = State()
    telefon = State()
    prava = State()


class EditClient(StatesGroup):
    ism = State()
    familiya = State()
    telefon = State()
    prava = State()


class Delete(StatesGroup):
    yes_or_no = State()
