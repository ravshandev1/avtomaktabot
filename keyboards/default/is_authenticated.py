from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_instructor = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👨‍✈️️Профил"),
            KeyboardButton(text="👨‍✈️Профилни ўзгартириш"),
        ],
        [
            KeyboardButton(text="👨‍✈️Профилни ўчириш"),
            KeyboardButton(text='Машғулот нархлари'),
        ],
        [
            # KeyboardButton(text="Балансни тўлдириш"),
            KeyboardButton(text="👨‍✈️Машғулотлар рўйхати"),
        ],
        # [
        #     KeyboardButton(text="Бот ҳисобингиздан оладиган хизмат ҳақи"),
        # ],
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
            KeyboardButton(text='Машғулот нархлари')
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
            KeyboardButton(text='Машғулот манзилини олиш'),
        ],
        [
            KeyboardButton(text="Бош меню")
        ]
    ],
    resize_keyboard=True
)
profile_delete = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ҳа'),
            KeyboardButton(text='Йўқ'),
        ]
    ],
    resize_keyboard=True
)

location_btn = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Манзилингизни юборинг!', request_location=True)
    ]
], resize_keyboard=True)
