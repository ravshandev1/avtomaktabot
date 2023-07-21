from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime


def create_callback_data(action, h, m):
    return f"{action};{h};{m}"


now = datetime.now()


def create_clock(lang=None, hr=None, mn=None):
    if hr is None:
        hr = now
    if mn is None:
        mn = datetime(1900, 1, 23, 0, 0)
    hr = datetime.strftime(hr, "%H")
    mn = datetime.strftime(mn, "%M")
    keyboard = list()
    # First row - ⬆️
    row = list()
    row.append(InlineKeyboardButton("⬆️", callback_data=create_callback_data("hour⬆️", hr, mn)))
    row.append(InlineKeyboardButton("⬆️", callback_data=create_callback_data("minute⬆️", hr, mn)))
    keyboard.append(row)
    # Second row - Hour Minute
    row = list()
    row.append(InlineKeyboardButton(f"{hr}", callback_data=create_callback_data("IGNORE", hr, mn)))
    row.append(InlineKeyboardButton(f"{mn}", callback_data=create_callback_data("IGNORE", hr, mn)))
    keyboard.append(row)
    # Third row - ⬇️
    row = list()
    row.append(InlineKeyboardButton("⬇️", callback_data=create_callback_data("hour⬇️", hr, mn)))
    row.append(InlineKeyboardButton("⬇️", callback_data=create_callback_data("minute⬇️", hr, mn)))
    keyboard.append(row)
    # Last row = OK
    row = list()
    row.append(InlineKeyboardButton("OK", callback_data=create_callback_data("OK", hr, mn)))
    keyboard.append(row)
    # Back button
    row = list()
    if lang == 'uz':
        row.append(InlineKeyboardButton("⬅️Oртга", callback_data=create_callback_data("⬅️Oртга", hr, mn)))
    else:
        row.append(InlineKeyboardButton("⬅️Назад", callback_data=create_callback_data("⬅️Назад", hr, mn)))
    keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
