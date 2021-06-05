import logging


class BaseController:
    __slots__ = ["logger"]

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(self.__class__.__name__)
