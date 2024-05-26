from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Optional, Any
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

from . import Model
from .mixins.dated import DatedMixin

class AlbumTypeTable(Model):
    __tablename__ = 'album_type'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]


class AlbumTable(Model, DatedMixin):
    __tablename__ = 'album'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    name: Mapped[str]
    description: Mapped[Optional[str]]
    is_public: Mapped[bool] = mapped_column(default=False, nullable=False)
    album_type_id: Mapped[int] = mapped_column(ForeignKey('album_type.id'))
    song_order: Mapped[Optional[JSONB]] = mapped_column(type_=JSONB)