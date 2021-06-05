from enum import IntEnum
from typing import Union

from pydantic import BaseSettings as PydanticBaseSettings
from pydantic import validator

__all__ = (
    "api_settings",
    "app_settings",
    "db_settings",
    "global_settings",
)


class Environment(IntEnum):
    TEST = 0
    DEV = 1
    PROD = 2

    @classmethod
    def get_env(cls, env: str):
        default_env = "development"
        return {
            "test": cls.TEST,
            "development": cls.DEV,
            "production": cls.PROD,
        }.get(env.lower(), default_env)


class BaseSettings(PydanticBaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


class GlobalSettings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    ENV: Union[Environment, str] = "development"
    WORKERS: int = 1

    @validator("ENV", pre=True)
    @classmethod
    def get_env(cls, value):
        return Environment.get_env(value)

    @validator("LOG_LEVEL")
    @classmethod
    def get_log_level(cls, value: str):
        return value.upper()

    @property
    def is_test(self):
        return self.ENV == Environment.TEST


global_settings = GlobalSettings()


class AppSettings(BaseSettings):
    NAME: str = "My Calendly"
    DESCRIPTION: str = "Open-source version of Calendly"
    SERVERS: list[dict[str, str]] = [{"url": "http://localhost:8000"}]
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True

    class Config(BaseSettings.Config):
        env_prefix = "APP_"


app_settings = AppSettings()


class DBSettings(BaseSettings):
    URI: str

    class Config(BaseSettings.Config):
        env_prefix = "DB_"


db_settings = DBSettings()


class ApiSettings(BaseSettings):
    API_STR: str = "/api"
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    BACKEND_CORS_METHODS: list[str] = ["*"]
    BACKEND_CORS_HEADERS: list[str] = ["*"]

    @validator("BACKEND_CORS_ORIGINS", pre=True, allow_reuse=True)
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, list[str]]) -> Union[list[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config(BaseSettings.Config):
        env_prefix = "API_"


api_settings = ApiSettings()
