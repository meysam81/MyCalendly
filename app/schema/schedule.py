from datetime import date, time

from .base import BaseModel, Field


class ScheduleDay(BaseModel):
    date: date
    start_ts: time = Field(example="09:00:00")
    end_ts: time = Field(example="17:00:00")


class ScheduleIn(BaseModel):
    name: str = Field(example="30 Minutes Talk")
    # TODO: make upper bound configurable
    timeframes: list[ScheduleDay] = Field(min_items=1, max_items=365)
