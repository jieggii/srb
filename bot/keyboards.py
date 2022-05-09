from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.models import Period

new_sub_select_period_kbd = ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
new_sub_select_period_kbd.add(
    KeyboardButton(Period.MONTH.capitalize()),
    KeyboardButton(Period.YEAR.capitalize()),
    KeyboardButton(Period.WEEK.capitalize()),
)

new_sub_last_charge_kbd = ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
new_sub_last_charge_kbd.add(KeyboardButton("Today"))
