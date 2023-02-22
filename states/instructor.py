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


class EditInstructor(StatesGroup):
    ism = State()
    familiya = State()
    telefon = State()
    jins = State()
    tuman = State()
    toifa = State()
    moshina = State()
    nomeri = State()


class Balans(StatesGroup):
    summa = State()
