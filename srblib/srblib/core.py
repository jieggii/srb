from datetime import datetime

from dateutil.relativedelta import relativedelta

from srblib.db.models import Period


def count_next_charge(last_charge: datetime, period: Period) -> datetime:
    match period:
        case Period.WEEK:
            next_charge = last_charge + relativedelta(weeks=1)
        case Period.ONE_MONTH:
            next_charge = last_charge + relativedelta(months=1)
        case Period.THREE_MONTHS:
            next_charge = last_charge + relativedelta(months=3)
        case Period.SIX_MONTHS:
            next_charge = last_charge + relativedelta(months=6)
        case Period.YEAR:
            next_charge = last_charge + relativedelta(years=1)
        case _:
            raise ValueError(f"{period} is not a valid period")
    return next_charge
