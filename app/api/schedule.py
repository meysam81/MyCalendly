from http import HTTPStatus

from app.controllers.schedule import ScheduleController
from app.models import schedule as schedule_model
from app.schema import schedule as schedule_schema

from . import api_doc_responses as common_responses
from .base import APIRouter, Body, Path, Query

router = APIRouter(prefix="/schedule")


@router.post(
    "",
    response_model=schedule_model.ScheduleModel,
    responses={
        **common_responses.bad_time_frame_provided,
    },
    status_code=HTTPStatus.CREATED,
)
async def create_schedule(schedule: schedule_schema.ScheduleIn):
    return ScheduleController.create_schedule(schedule)


@router.get(
    "",
    response_model=list[schedule_model.ScheduleModel],
    status_code=HTTPStatus.OK,
)
async def list_schedules(
    offset: int = Query(ge=0, default=0),
    limit: int = Query(default=10, ge=1, le=50),
):
    return ScheduleController.list_schedules(offset=offset, limit=limit)


@router.get(
    "/{schedule_id}",
    response_model=schedule_model.ScheduleModel,
    responses={
        **common_responses.not_found,
    },
    status_code=HTTPStatus.OK,
)
async def retrieve_schedule(schedule_id: int = Path(..., ge=1)):
    return ScheduleController.retrieve_schedule(schedule_id)


@router.delete(
    "/{schedule_id}",
    responses={
        **common_responses.not_found,
    },
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_schedule(schedule_id: int = Path(..., ge=1)):
    ScheduleController.delete_schedule(schedule_id)


@router.patch(
    "/{schedule_id}",
    responses={
        **common_responses.not_found,
        **common_responses.bad_time_frame_provided,
    },
    response_model=schedule_model.ScheduleModel,
    status_code=HTTPStatus.OK,
)
async def update_schedule(
    schedule_id: int = Path(..., ge=1),
    schedule: schedule_schema.ScheduleUpdateIn = Body(...),
):
    return ScheduleController.update_schedule(schedule_id, schedule)
