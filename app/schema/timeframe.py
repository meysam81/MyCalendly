from datetime import date, time

from pydantic import BaseModel


class TimeFrame(BaseModel):
    day: date
    start_ts: time
    end_ts: time


class ScheduleIn(BaseModel):
    timeframes: list[TimeFrame]
