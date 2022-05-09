from datetime import datetime

from dateutil.relativedelta import relativedelta

from bot.models import Period


def get_next_charge(last_charge: datetime, period: Period) -> datetime:
    match period:
        case Period.WEEK:
            next_charge = last_charge + relativedelta(weeks=1)
        case Period.MONTH:
            next_charge = last_charge + relativedelta(months=1)
        case Period.YEAR:
            next_charge = last_charge + relativedelta(years=1)
        case _:
            raise ValueError("Invalid period")
    return next_charge
