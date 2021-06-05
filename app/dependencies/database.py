from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import db_settings

SQLALCHEMY_DATABASE_URL = db_settings.URI

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
db = SessionLocal()


__all__ = [
    "Base",
    "Column",
    "DateTime",
    "db",
    "Integer",
    "String",
]
