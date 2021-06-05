import asyncio
from datetime import datetime
from functools import wraps
from logging import Logger


class Metrics:
    __slots__ = ["values", "logger", "with_duration", "exec_start"]

    def __init__(self, logger: Logger, with_duration: bool = False):
        self.values = {}
        self.logger = logger
        self.with_duration = with_duration
        self.exec_start = None

    def set(self, **metrics):
        self.values.update(metrics)

    def __enter__(self):
        if self.with_duration:
            self.exec_start = datetime.utcnow()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.with_duration:
            self.values["exec_duration"] = (
                datetime.utcnow() - self.exec_start
            ).total_seconds()
        self.logger.info(f"[metrics] {self.values}")

    @classmethod
    def capture(cls, logger: Logger, with_duration=False):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                with cls(logger, with_duration=with_duration) as metrics:
                    kwargs.update(metrics=metrics)
                    if asyncio.iscoroutinefunction(func):
                        return await func(*args, **kwargs)
                    return func(*args, **kwargs)

            return wrapper

        return decorator
