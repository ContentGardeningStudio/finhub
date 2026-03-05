from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .settings import settings


# SQLite needs special flag for multi-threaded apps
engine = create_engine(
    settings.db_url,
    connect_args={"check_same_thread": False}
    if settings.db_url.startswith("sqlite")
    else {},
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
