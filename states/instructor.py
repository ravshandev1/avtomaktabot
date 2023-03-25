from aiogram.dispatcher.filters.state import State, StatesGroup


class InstructorForm(StatesGroup):
    ism = State()
    familiya = State()
    telefon = State()
    jins = State()
    tuman = State()
    toifa = State()
    moshina = State()
    nomeri = State()
    card = State()
    location = State()


class EditInstructor(StatesGroup):
    ism = State()
    familiya = State()
    telefon = State()
    jins = State()
    tuman = State()
    toifa = State()
    moshina = State()
    nomeri = State()
    location = State()
    card = State()


class Balans(StatesGroup):
    summa = State()


class DeleteIns(StatesGroup):
    yes_or_no = State()
