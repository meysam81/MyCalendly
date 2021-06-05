from pydantic import BaseModel as _PydanticBaseModel
from pydantic import validator


class BaseModel(_PydanticBaseModel):
    class Config:
        orm_mode = True


__all__ = (
    "BaseModel",
    "validator",
)
