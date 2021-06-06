import abc
from http import HTTPStatus

from .base import HTTPException


class BaseException_(HTTPException, metaclass=abc.ABCMeta):
    def __init__(self, detail):
        self.detail = detail


class EntityNotFound(BaseException_):
    status_code = HTTPStatus.NOT_FOUND
