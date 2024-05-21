from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Optional

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
    type: Mapped[int] = mapped_column(ForeignKey('album_type.id'))
    song_order: Mapped[Optional[JSON]]