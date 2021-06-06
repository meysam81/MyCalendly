import logging
from datetime import date, datetime, time
from functools import reduce

from timeframe import BatchTimeFrame, TimeFrame

from app.common import exceptions
from app.dependencies.database import Base as BaseORMModel
from app.dependencies.database import Column, DateTime, Integer, String, db

from .base import BaseModel, validator

logger = logging.getLogger(__file__)

# =============================================================================
# =============================== ORM Objects =================================
# =============================================================================


class _ScheduleORM(BaseORMModel):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    timeframes = Column(String(2 ** 15), nullable=False)
    created_ts = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_ts = Column(DateTime, nullable=False, default=datetime.utcnow)


# =============================================================================
# =============================== App Entities ================================
# =============================================================================


class ScheduleDay(BaseModel):
    date: date
    start_ts: time
    end_ts: time


class ScheduleModel(BaseModel):
    id: int
    name: str
    timeframes: list[ScheduleDay]
    created_ts: datetime
    updated_ts: datetime

    @validator("timeframes", pre=True)
    @classmethod
    def deserialize_timeframes(cls, value):
        if isinstance(value, list):
            return value
        if not isinstance(value, str):
            raise TypeError(f"Expected str but got: {type(value)}")
        return cls._deserialize_timeframes(value)

    @classmethod
    def create_schedule(cls, name, timeframes):
        try:
            schedule = _ScheduleORM(
                name=name,
                timeframes=cls._serialize_timeframes(timeframes),
            )
            db.add(schedule)
            db.commit()
            return cls.from_orm(schedule)
        except Exception as exp:
            logger.error(exp)
            db.rollback()
            raise

    @classmethod
    def list_schedules(cls, offset, limit):
        result = (
            db.query(_ScheduleORM)
            .order_by(_ScheduleORM.updated_ts.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return list(map(cls.from_orm, result))

    @classmethod
    def retrieve_schedule(cls, schedule_id):
        try:
            schedule = db.query(_ScheduleORM).get(schedule_id)
            if schedule is None:
                raise exceptions.EntityNotFound(f"Schedule not found: {schedule_id}")
            return cls.from_orm(schedule)
        except Exception as exp:
            logger.error(exp)
            raise

    @classmethod
    def hard_delete_schedule(cls, schedule_id):
        # TODO: do a soft delete
        try:
            result = (
                db.query(_ScheduleORM).filter(_ScheduleORM.id == schedule_id).delete()
            )
            if not result:
                raise exceptions.EntityNotFound(f"Schedule not found: {schedule_id}")
            db.commit()
        except Exception as exp:
            logger.error(exp)
            db.rollback()
            raise

    @classmethod
    def update_schedule(cls, schedule_id, name=None, timeframes=None):
        try:
            schedule = db.query(_ScheduleORM).get(schedule_id)
            if schedule is None:
                raise exceptions.EntityNotFound(f"Schedule not found: {schedule_id}")

            changed = False
            if name is not None:
                changed = True
                schedule.name = name
            if timeframes is not None:
                changed = True
                schedule.timeframes = cls._serialize_timeframes(timeframes)
            if changed:
                schedule.updated_ts = datetime.utcnow()
            db.commit()

            return cls.from_orm(schedule)
        except Exception as exp:
            logger.error(exp)
            db.rollback()
            raise

    @staticmethod
    def _serialize_timeframes(schedule_days: list[ScheduleDay]) -> str:
        # TODO: this should be done in the library of `timeframe`
        def convert_to_timeframe(schedule_day):
            start_ts = datetime.combine(schedule_day.date, schedule_day.start_ts)
            end_ts = datetime.combine(schedule_day.date, schedule_day.end_ts)
            return TimeFrame(start_ts, end_ts)

        timeframes = map(convert_to_timeframe, schedule_days)
        batch_timeframes = reduce(lambda x, y: x + y, timeframes, next(timeframes))
        if isinstance(batch_timeframes, BatchTimeFrame):
            return ",".join((map(repr, batch_timeframes)))
        return repr(batch_timeframes)

    @staticmethod
    def _deserialize_timeframes(raw_timeframes: str) -> list[ScheduleDay]:
        # TODO: this should be done in the library of `timeframe`
        result = []
        for timeframe in raw_timeframes.split(","):
            bounds = timeframe.split("#")
            start_ts, end_ts = tuple(map(datetime.fromisoformat, bounds))
            result.append(
                ScheduleDay(
                    date=start_ts.date(),
                    start_ts=start_ts.time(),
                    end_ts=end_ts.time(),
                )
            )
        return result
