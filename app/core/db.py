import os
from typing import Iterator

from sqlmodel import create_engine, SQLModel, Session

from app.core.config import settings

raw_url = os.environ["DATABASE_URL"]

if raw_url.startswith("postgres://"):
    url = "postgresql+psycopg://" + raw_url[len("postgres://"):]
elif raw_url.startswith("postgresql://"):
    url = "postgresql+psycopg://" + raw_url[len("postgresql://"):]
else:
    url = raw_url

engine = create_engine(url, pool_pre_ping=True)


# engine = create_engine(settings.DATABASE_URL, echo=False,
#                       connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {})


def init_db() -> None:
    if settings.ENVIRONMENT == "DEV":
        SQLModel.metadata.create_all(engine)  # dev


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
