from datetime import date, time
from typing import Optional

from .base import BaseModel, Field


class ScheduleDay(BaseModel):
    date: date
    start_ts: time = Field(example="09:00:00")
    end_ts: time = Field(example="17:00:00")

    def __str__(self):
        return str({k: str(v) for k, v in self.dict().items()})


class ScheduleIn(BaseModel):
    # TODO: make min-length configurable
    name: str = Field(example="30 Minutes Talk", min_length=3)
    # TODO: make upper bound configurable
    timeframes: list[ScheduleDay] = Field(min_items=1, max_items=365)


class ScheduleUpdateIn(BaseModel):
    name: Optional[str] = Field(example="30 Minutes Talk", min_length=3)
    # TODO: make upper bound configurable
    timeframes: Optional[list[ScheduleDay]] = Field(min_items=1, max_items=365)
