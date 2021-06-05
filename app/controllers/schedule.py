from app.models.schedule import ScheduleModel
from app.schema import schedule as schedule_schema

from .base import BaseController


class ScheduleController(BaseController):
    @staticmethod
    def create_schedule(schedule: schedule_schema):
        return ScheduleModel.create_schedule(
            name=schedule.name, timeframes=schedule.timeframes
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

    @staticmethod
    def update_schedule(schedule_id, schedule):
        return ScheduleModel.update_schedule(
            schedule_id, name=schedule.name, timeframes=schedule.timeframes
        )
