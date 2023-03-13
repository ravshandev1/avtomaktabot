from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_instructor = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🧑‍✈️Профил"),
            KeyboardButton(text="🧑‍✈️Профилни ўзгартириш"),
        ],
        [
            KeyboardButton(text="Балансни тўлдириш"),
            KeyboardButton(text="🧑‍✈️Машғулотлар рўйхати"),
        ],
        [
            KeyboardButton(text="Профилни ўчириш"),
            KeyboardButton(text='Нарх ва фоизлар')
        ]
    ],
    resize_keyboard=True
)

menu_client = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Профил"),
            KeyboardButton(text="Профилни ўзгартириш"),
        ],
        [
            KeyboardButton(text="Профилни ўчириш"),
            KeyboardButton(text="Машғулот"),
        ],
        [
            KeyboardButton(text='Нархлар')
        ]
    ],
    resize_keyboard=True
)
action_session = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Машғулотлар рўйхати"),
            KeyboardButton(text="Машғулот яратиш"),
        ],
        [
            KeyboardButton(text="Бош меню")
        ]
    ],
    resize_keyboard=True
)

sessions = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Бўлиб утган"),
            KeyboardButton(text="Бўлиши керак"),
        ],
        [
            KeyboardButton(text="Бош меню"),
            KeyboardButton(text="⬅️Oртга"),
        ]
    ],
    resize_keyboard=True
)

edit_session = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Машғулотни бекор килиш'),
        ],
        [
            KeyboardButton(text="Бош меню")
        ]
    ],
    resize_keyboard=True
)

location_btn = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Манзилингизни юборинг!', request_location=True)
    ]
], resize_keyboard=True)
