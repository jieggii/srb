from datetime import datetime
from typing import Optional

from bot.models import Period


def raw_last_charge_date_to_datetime(text: str) -> Optional[datetime]:
    try:
        return datetime.strptime(text, "%d.%m.%Y")
    except ValueError:
        return None


def raw_period_to_period(text: str) -> Optional[Period]:
    try:
        return Period(text.lower())
    except ValueError:
        return None
