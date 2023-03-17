from aiogram.dispatcher.filters.state import State, StatesGroup


class SessionForm(StatesGroup):
    tuman = State()
    toifa = State()
    jins = State()
    moshina = State()
    instructor = State()
    kun = State()
    vaqt = State()
    tulov_turi = State()


class SessionEdit(StatesGroup):
    start = State()
    finish = State()
