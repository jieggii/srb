from datetime import datetime
from enum import Enum
from typing import List, Optional

from beanie import Document, Indexed
from pydantic import BaseModel


class Period(str, Enum):
    WEEK = "week"
    ONE_MONTH = "month"
    THREE_MONTHS = "3 months"
    SIX_MONTHS = "6 months"
    YEAR = "year"


class Sub(BaseModel):
    name: str
    amount: str
    period: Period
    last_charge: datetime
    last_notification: Optional[datetime]

    def __str__(self):
        return (
            "Sub("
            f"name={self.name}, "
            f"amount={self.amount}, "
            f"period={self.period}, "
            f"last_charge={self.last_charge}, "
            f"last_notification={self.last_notification}"
            ")"
        )


class User(Document):
    user_id: Indexed(int)
    subs: Optional[List[Sub]]

    class Collection:
        name = "users"

    def __str__(self):
        return f"User(user_id={self.user_id}, subs=[...]({len(self.subs)}))"
