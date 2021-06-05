from http import HTTPStatus

from fastapi import APIRouter

from app.controllers.schedule import ScheduleController
from app.models import schedule as schedule_model
from app.schema import schedule as schedule_schema

router = APIRouter()


@router.post(
    "/schedule",
    response_model=schedule_model.ScheduleModel,
    status_code=HTTPStatus.CREATED,
)
async def create_schedule(schedule: schedule_schema.ScheduleIn):
    return ScheduleController.create_schedule(schedule)
