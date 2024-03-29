from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import datetime
import calendar


def create_callback_data(action, year, month, day):
    """ Create the callback data associated to each button"""
    return action + ";" + str(year) + ";" + str(month) + ";" + str(day)


def create_calendar(lang=None, year=None, month=None):
    """
    Create an inline keyboard with the provided year and month
    :param int year: Year to use in the calendar, if None the current year is used.
    :param int month: Month to use in the calendar, if None the current month is used.
    :return: Returns the InlineKeyboardMarkup object with the calendar.
    """
    now = datetime.datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    if lang is None:
        lang = 'ru'
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboard = list()
    # First row - Month and Year
    row = list()
    row.append(InlineKeyboardButton(calendar.month_name[month] + " " + str(year), callback_data=data_ignore))
    keyboard.append(row)
    # Second row - Week Days
    row = list()
    for day in ["Dush", "Sesh", "Chor", "Pay", "Jum", "Shan", "Yak"]:
        row.append(InlineKeyboardButton(day, callback_data=data_ignore))
    keyboard.append(row)
    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
            else:
                row.append(InlineKeyboardButton(str(day), callback_data=create_callback_data("DAY", year, month, day)))
        keyboard.append(row)
    # Last row - Buttons
    row = list()
    row.append(InlineKeyboardButton("<<", callback_data=create_callback_data("PREV-MONTH", year, month, day)))
    row.append(InlineKeyboardButton(">>", callback_data=create_callback_data("NEXT-MONTH", year, month, day)))
    keyboard.append(row)
    # Back button
    row = list()
    if lang == 'uz':
        row.append(InlineKeyboardButton("⬅️Oртга", callback_data=create_callback_data("⬅️Oртга", year, month, day)))
    else:
        row.append(InlineKeyboardButton("⬅️Назад", callback_data=create_callback_data("⬅️Назад", year, month, day)))
    keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def call_data(data):
    return data.split(";")
