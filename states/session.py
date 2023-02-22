from aiogram.dispatcher.filters.state import State, StatesGroup


class SessionForm(StatesGroup):
    toifa = State()
    jins = State()
    moshina = State()
    instructor = State()
    qayerdan = State()
    kun = State()
    vaqt = State()
    tulov_turi = State()


class SessionEdit(StatesGroup):
    start = State()
    finish = State()
