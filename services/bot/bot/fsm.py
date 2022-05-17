from aiogram.dispatcher.filters.state import State, StatesGroup


class NewSub(StatesGroup):
    name = State()
    period = State()
    amount = State()
    last_charge = State()
