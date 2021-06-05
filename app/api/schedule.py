from http import HTTPStatus

from fastapi import APIRouter

from app.schema import timeframe

router = APIRouter()


@router.post("/schedule", status_code=HTTPStatus.CREATED)
async def create_schedule(timeframe: timeframe.ScheduleIn):
    return timeframe
