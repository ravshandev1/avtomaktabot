from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

sessions = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Бўлиб ўтган", callback_data='before')
        ],
        [
            InlineKeyboardButton(text="Бўлиши керак", callback_data='after')
        ]
    ]
)


def create_after_sessions_for_ins(response: dict, page: int):
    keyboard = list()
    row = list()
    for (i, obj) in zip(range(1, response['count'] + 1), response['results']):
        row.append(InlineKeyboardButton(text=f"{i}", callback_data=f"id:{obj['id']}"))
    keyboard.append(row)
    row = list()
    row.append(InlineKeyboardButton(text='⬅️', callback_data=f"previous:{page}"))
    row.append(InlineKeyboardButton(text='➡️', callback_data=f"next:{page}"))
    keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def before_sessions_for_ins(page):
    keyboard = list()
    row = list()
    row.append(InlineKeyboardButton(text='⬅️', callback_data=f'oldingi:{page}'))
    row.append(InlineKeyboardButton(text='➡️', callback_data=f'keyingi:{page}'))
    keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_after_sessions_for_cl(response: dict, page: int):
    keyboard = list()
    row = list()
    for (i, obj) in zip(range(1, response['count'] + 1), response['results']):
        row.append(InlineKeyboardButton(text=f"{i}", callback_data=f"scl:{obj['id']}"))
    keyboard.append(row)
    row = list()
    row.append(InlineKeyboardButton(text='⬅️', callback_data=f"rav:{page}"))
    row.append(InlineKeyboardButton(text='➡️', callback_data=f"bob:{page}"))
    keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def before_sessions_for_cl(page):
    keyboard = list()
    row = list()
    row.append(InlineKeyboardButton(text='⬅️', callback_data=f'jal:{page}'))
    row.append(InlineKeyboardButton(text='➡️', callback_data=f'kam:{page}'))
    keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


rate = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='1😣', callback_data='juda_yomon'),
            InlineKeyboardButton(text='2😔', callback_data='yomon'),
        ],
        [
            InlineKeyboardButton(text='3😑', callback_data='qoniqarli'),
            InlineKeyboardButton(text='4🙂', callback_data='yaxshi'),
        ],
        [
            InlineKeyboardButton(text='5😁', callback_data='zur')
        ]
    ]
)
