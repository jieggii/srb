from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from srblib.db.models import Period

new_sub_select_period_kbd = ReplyKeyboardMarkup(one_time_keyboard=True, row_width=3)
new_sub_select_period_kbd.add(
    KeyboardButton(Period.ONE_MONTH.capitalize()),
    KeyboardButton(Period.THREE_MONTHS.capitalize()),
    KeyboardButton(Period.SIX_MONTHS.capitalize()),
    KeyboardButton(Period.WEEK.capitalize()),
    KeyboardButton(Period.YEAR.capitalize()),
)

new_sub_last_charge_kbd = ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
new_sub_last_charge_kbd.add(KeyboardButton("Today"))
