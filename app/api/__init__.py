from fastapi import APIRouter

from . import schedule

router = APIRouter()


router.include_router(schedule.router, tags=["Scheduling"])
