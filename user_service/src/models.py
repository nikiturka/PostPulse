import datetime
from typing import Annotated

from sqlalchemy import String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[Annotated[int, mapped_column(primary_key=True)]]
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    surname: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]]
    updated_at: Mapped[
        Annotated[
            datetime.datetime,
            mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow)
        ]
    ]
