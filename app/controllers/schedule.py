from datetime import datetime

from app.common import exceptions
from app.models.schedule import ScheduleModel
from app.schema import schedule as schedule_schema

from .base import BaseController


class ScheduleController(BaseController):
    @classmethod
    def create_schedule(cls, schedule: schedule_schema.ScheduleIn):
        allowed_timeframes = cls.check_valid_timeframes(schedule.timeframes)

        if not allowed_timeframes:  # this shouldn't happen in theory
            err = "No valid schedule was provided"
            raise exceptions.BadTimeFrameProvided(err)

        return ScheduleModel.create_schedule(
            name=schedule.name,
            description=schedule.description,
            duration=schedule.duration,
            timeframes=allowed_timeframes,
        )

    @staticmethod
    def list_schedules(offset, limit):
        return ScheduleModel.list_schedules(offset=offset, limit=limit)

    @staticmethod
    def retrieve_schedule(schedule_id):
        return ScheduleModel.retrieve_schedule(schedule_id)

    @staticmethod
    def delete_schedule(schedule_id):
        return ScheduleModel.hard_delete_schedule(schedule_id)

    @classmethod
    def update_schedule(cls, schedule_id, schedule: schedule_schema.ScheduleUpdateIn):
        allowed_timeframes = cls.check_valid_timeframes(schedule.timeframes)
        return ScheduleModel.update_schedule(
            schedule_id,
            name=schedule.name,
            description=schedule.description,
            duration=schedule.duration,
            timeframes=allowed_timeframes,
        )

    @staticmethod
    def check_valid_timeframes(timeframes: schedule_schema.ScheduleDay):
        allowed_timeframes = []
        for timeframe in timeframes:
            if not (timeframe.end_ts > timeframe.start_ts):
                err = f"start_ts should be lower than end_ts: {timeframe}"
                raise exceptions.BadTimeFrameProvided(err)

            start_dt = datetime.combine(timeframe.date, timeframe.start_ts)
            if start_dt > datetime.utcnow():
                allowed_timeframes.append(timeframe)
            else:
                err = f"Only future schedules are accepted: {timeframe}"
                raise exceptions.BadTimeFrameProvided(err)

        return allowed_timeframes
