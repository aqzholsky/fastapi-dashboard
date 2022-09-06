from typing import Optional

from pydantic import BaseModel


class DailyRequestsByStatus(BaseModel):
    status: Optional[str] = None
    count: Optional[int] = None


class DailyRequestsOfLastMonth(BaseModel):
    date: Optional[str] = None
    count: Optional[int] = None
