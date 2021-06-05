from app.models.schedule import ScheduleModel
from app.schema import schedule as schedule_schema

from .base import BaseController


class ScheduleController(BaseController):
    @staticmethod
    def create_schedule(schedule: schedule_schema):
        return ScheduleModel.create_schedule(schedule.name, schedule.timeframes)
