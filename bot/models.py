import datetime
from enum import Enum
from typing import List, Optional

from beanie import Document, Indexed
from pydantic import BaseModel


class Period(str, Enum):
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class Sub(BaseModel):
    name: str
    amount: str
    next_charge: datetime.datetime
    period: Period


class User(Document):
    user_id: Indexed(int)
    subs: Optional[List[Sub]]

    class Collection:
        name = "users"
