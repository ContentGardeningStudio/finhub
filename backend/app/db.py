from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .settings import get_settings


class Base(DeclarativeBase):
    pass


def get_engine():
    settings = get_settings()
    is_sqlite = settings.database_url.startswith("sqlite")

    return create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False} if is_sqlite else {},
    )


def get_session_local():
    return sessionmaker(
        bind=get_engine(),
        autoflush=False,
        autocommit=False,
    )


def get_db():
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()