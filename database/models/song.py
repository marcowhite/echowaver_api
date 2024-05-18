from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from datetime import datetime
from typing_extensions import Optional

from base import Model


class SongTable(Model):
    __tablename__ = 'songs'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = relationship(foreign_keys='users.id')
    path: Mapped[str]

    name: Mapped[str]
    description: Mapped[Optional[str]]
    genre: Mapped[Optional[str]]
    public: Mapped[bool] = mapped_column(default=False)
    background: Mapped[str]
    cover: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(default=func.now())


class ListeningsTable(Model):
    __tablename__ = 'listenings'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = relationship(foreign_keys='users.id')
    origin_country_id: Mapped[int] = relationship(foreign_keys='countries.id')
