from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from datetime import datetime
from typing_extensions import Optional

from base import Model


class AlbumTypeTable(Model):
    __tablename__ = 'album_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]


class AlbumTable(Model):
    __tablename__ = 'albums'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = relationship(foreign_keys='users.id')

    name: Mapped[str]
    description: Mapped[Optional[str]]
    public: Mapped[bool] = mapped_column(default=False)
    type: Mapped[int] = relationship(foreign_keys='album_types.id')

    # songs_order: JSONB

    created_at: Mapped[datetime] = mapped_column(default=func.now())
