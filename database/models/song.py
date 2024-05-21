from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Optional

from . import Model
from .mixins.dated import DatedMixin


class SongTable(Model, DatedMixin):
    __tablename__ = 'song'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    path: Mapped[str]

    is_public: Mapped[bool] = mapped_column(default=False, nullable=False)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    genre: Mapped[Optional[str]]
    cover: Mapped[Optional[str]]

    background: Mapped[Optional[str]]


class SongListenTable(Model, DatedMixin):
    __tablename__ = 'song_listen'

    id: Mapped[int] = mapped_column(primary_key=True)
    song_id: Mapped[int] = mapped_column(ForeignKey('song.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    origin_country_id: Mapped[int] = mapped_column(ForeignKey('country.id'))
    meta: Mapped[Optional[str]]


class SongTagTable(Model):
    __tablename__ = 'song_tag'
    id: Mapped[int] = mapped_column(primary_key=True)
    song_id: Mapped[int] = mapped_column(ForeignKey('song.id'))
    tag: Mapped[str]
